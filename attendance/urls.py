
from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance_dashboard'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path(
        'report/',
        views.monthly_attendance_report,
        name='monthly_attendance_report'
    ),
    path(
        'analytics/',
        views.analytics_dashboard,
        name='analytics_dashboard'
    ),
    path(
    'student-report/',
    views.student_attendance_report,
    name='student_attendance_report'
),
]
