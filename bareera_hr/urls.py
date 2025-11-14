from django.contrib import admin
from django.urls import path
from hr import views

urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('', views.user_login, name='root_login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # Admin Dashboard
    path('home/', views.home, name='home'),

    # Employee Dashboard
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:emp_id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),

    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),

    # Payroll
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/add/', views.add_payroll, name='add_payroll'),

    # CSV Export
    path('export-employees/', views.export_employees_csv, name='export_employees_csv'),
]
