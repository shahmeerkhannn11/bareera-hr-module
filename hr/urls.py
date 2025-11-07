from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Employees
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:emp_id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('employees/export/', views.export_employees_csv, name='export_employees_csv'),

    # Attendance & Payroll
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('payroll/', views.payroll_list, name='payroll_list'),
]
