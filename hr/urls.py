from django.urls import path
from . import views

urlpatterns = [
    # LOGIN / LOGOUT
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # SIGNUP
    path("signup/", views.signup, name="signup"),

    # ADMIN DASHBOARD
    path("", views.home, name="home"),

    # EMPLOYEE DASHBOARD
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),

    # EMPLOYEE CRUD
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.add_employee, name="add_employee"),
    path("employees/edit/<int:emp_id>/", views.edit_employee, name="edit_employee"),
    path("employees/delete/<int:emp_id>/", views.delete_employee, name="delete_employee"),

    # ATTENDANCE
    path("attendance/", views.attendance_list, name="attendance_list"),
    path("attendance/add/", views.add_attendance, name="add_attendance"),

    # PAYROLL
    path("payroll/", views.payroll_list, name="payroll_list"),
    path("payroll/add/", views.add_payroll, name="add_payroll"),

    # CSV EXPORT
    path("export-employees/", views.export_employees_csv, name="export_employees_csv"),
]
