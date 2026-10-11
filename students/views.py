
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import StudentForm


@login_required
def dashboard(request):
    query = request.GET.get('q', '').strip()

    students = Student.objects.all().order_by('roll_number')

    if query:
        students = students.filter(
            name__icontains=query
        ) | students.filter(
            roll_number__icontains=query
        ) | students.filter(
            course__icontains=query
        )

    context = {
        'students': students,
        'total_students': Student.objects.count(),
        'query': query,
    }

    return render(
        request,
        'students/dashboard.html',
        context
    )


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Student added successfully!'
            )
            return redirect('dashboard')
    else:
        form = StudentForm()

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Add New Student',
        }
    )


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Student updated successfully!'
            )
            return redirect('dashboard')
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Edit Student',
        }
    )


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()
        messages.success(
            request,
            'Student deleted successfully!'
        )
        return redirect('dashboard')

    return render(
        request,
        'students/confirm_delete.html',
        {'student': student}
    )
