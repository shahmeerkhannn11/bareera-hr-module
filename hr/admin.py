from django.contrib import admin
from .models import Employee, Attendance, Payroll

admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Payroll)
