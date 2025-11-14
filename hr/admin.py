from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import Employee, EmployeeProfile, Attendance, Payroll


# ---------------------------------------------------
#  Custom Admin Site
# ---------------------------------------------------
class HRAdminSite(admin.AdminSite):
    site_header = "👨‍💼 Bareera HR Administration"
    site_title = "Bareera HR Management"
    index_title = "HR Admin Dashboard"


admin_site = HRAdminSite(name="hr_admin")


# ---------------------------------------------------
# Register Django User model (so "Users" appears)
# ---------------------------------------------------
admin_site.register(User, UserAdmin)
admin_site.register(Group)


# ---------------------------------------------------
# Register your HR models
# ---------------------------------------------------
admin_site.register(Employee)
admin_site.register(EmployeeProfile)
admin_site.register(Attendance)
admin_site.register(Payroll)

from django.contrib import admin
from .models import Employee, EmployeeProfile, Attendance, Payroll


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_id", "name", "department", "position", "email", "salary", "date_joined")
    search_fields = ("name", "email", "department", "position")


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "employee")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status")
    list_filter = ("status", "date")


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ("employee", "amount", "payment_date")
    list_filter = ("payment_date",)
