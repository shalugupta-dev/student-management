
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.utils import timezone

from students.models import Student
from .models import Attendance


@login_required
def attendance_dashboard(request):
    """Show attendance dashboard summary."""
    today = timezone.localdate()

    total_students = Student.objects.count()
    today_records = Attendance.objects.filter(date=today)

    present_count = today_records.filter(status='Present').count()
    absent_count = today_records.filter(status='Absent').count()
    late_count = today_records.filter(status='Late').count()

    context = {
        'total_students': total_students,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'today': today,
        'today_records': today_records.select_related('student'),
    }

    return render(request, 'attendance/dashboard.html', context)


@login_required
def mark_attendance(request):
    """Mark or update attendance for a student on a date."""
    students = Student.objects.order_by('roll_number')

    if request.method == 'POST':
        student_id = request.POST.get('student')
        attendance_date = request.POST.get('date')
        status = request.POST.get('status')

        if not student_id or not attendance_date or not status:
            messages.error(
                request,
                'Please fill in all attendance fields.'
            )
            return redirect('mark_attendance')

        if status not in ['Present', 'Absent', 'Late']:
            messages.error(request, 'Invalid attendance status.')
            return redirect('mark_attendance')

        try:
            selected_student = Student.objects.get(pk=student_id)
            selected_date = date.fromisoformat(attendance_date)
        except (Student.DoesNotExist, ValueError):
            messages.error(request, 'Invalid student or date.')
            return redirect('mark_attendance')

        Attendance.objects.update_or_create(
            student=selected_student,
            date=selected_date,
            defaults={'status': status},
        )

        messages.success(request, 'Attendance saved successfully.')
        return redirect('attendance_dashboard')

    context = {
        'students': students,
        'today': timezone.localdate(),
    }

    return render(
        request,
        'attendance/mark_attendance.html',
        context
    )


@login_required
def monthly_attendance_report(request):
    """Show attendance records for the selected month."""
    today = timezone.localdate()
    selected_month = request.GET.get(
        'month',
        today.strftime('%Y-%m')
    )

    try:
        year, month = map(int, selected_month.split('-'))

        if not 1 <= month <= 12:
            raise ValueError

        start_date = date(year, month, 1)

        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

    except (ValueError, TypeError):
        selected_month = today.strftime('%Y-%m')
        start_date = date(today.year, today.month, 1)

        if today.month == 12:
            end_date = date(today.year + 1, 1, 1)
        else:
            end_date = date(today.year, today.month + 1, 1)

    records = Attendance.objects.filter(
        date__gte=start_date,
        date__lt=end_date,
    ).select_related(
        'student'
    ).order_by(
        'date',
        'student__roll_number'
    )

    context = {
        'records': records,
        'selected_month': selected_month,
        'total_records': records.count(),
        'present_count': records.filter(status='Present').count(),
        'absent_count': records.filter(status='Absent').count(),
        'late_count': records.filter(status='Late').count(),
    }

    return render(
        request,
        'attendance/monthly_report.html',
        context
    )


@login_required
def analytics_dashboard(request):
    """Show overall attendance analytics."""
    total_students = Student.objects.count()
    total_records = Attendance.objects.count()

    status_counts = Attendance.objects.values(
        'status'
    ).annotate(
        count=Count('id')
    )

    status_counts_dict = {
        'Present': 0,
        'Absent': 0,
        'Late': 0,
    }

    for item in status_counts:
        status_counts_dict[item['status']] = item['count']

    attended_count = (
        status_counts_dict['Present']
        + status_counts_dict['Late']
    )

    if total_records:
        attendance_percentage = round(
            attended_count / total_records * 100,
            2
        )
    else:
        attendance_percentage = 0

    monthly_counts = []
    current_month = timezone.localdate().replace(day=1)

    for offset in range(5, -1, -1):
        month_index = current_month.month - offset
        year = current_month.year

        while month_index <= 0:
            month_index += 12
            year -= 1

        month_start = date(year, month_index, 1)

        if month_index == 12:
            month_end = date(year + 1, 1, 1)
        else:
            month_end = date(year, month_index + 1, 1)

        count = Attendance.objects.filter(
            date__gte=month_start,
            date__lt=month_end,
        ).count()

        monthly_counts.append({
            'month': month_start.strftime('%b %Y'),
            'count': count,
        })

    recent_records = Attendance.objects.select_related(
        'student'
    ).order_by(
        '-date',
        '-created_at'
    )[:8]

    context = {
        'total_students': total_students,
        'total_records': total_records,
        'status_counts': status_counts_dict,
        'attendance_percentage': attendance_percentage,
        'monthly_counts': monthly_counts,
        'recent_records': recent_records,
    }

    return render(
        request,
        'attendance/analytics.html',
        context
    )


@login_required
def student_attendance_report(request):
    """Show attendance percentage for each student."""
    students = Student.objects.annotate(
        total_classes=Count('attendance_records'),
        attended_classes=Count(
            'attendance_records',
            filter=Q(
                attendance_records__status__in=['Present', 'Late']
            )
        ),
    ).order_by('roll_number')

    good_attendance_count = 0
    low_attendance_count = 0
    no_attendance_count = 0

    for student in students:
        if student.total_classes:
            student.attendance_percentage = round(
                student.attended_classes
                / student.total_classes * 100,
                2
            )

            if student.attendance_percentage < 75:
                low_attendance_count += 1
            else:
                good_attendance_count += 1
        else:
            student.attendance_percentage = None
            no_attendance_count += 1

    context = {
        'students': students,
        'total_students': students.count(),
        'good_attendance_count': good_attendance_count,
        'low_attendance_count': low_attendance_count,
        'no_attendance_count': no_attendance_count,
    }

    return render(
        request,
        'attendance/student_report.html',
        context
    )
