from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'date',
        'status',
        'updated_at',
    )

    list_filter = ('date', 'status')
    search_fields = (
        'student__name',
        'student__roll_number',
    )

    date_hierarchy = 'date'