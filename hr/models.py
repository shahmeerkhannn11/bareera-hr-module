from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_joined = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.position})"


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.employee.name} Profile"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present','Present'), ('Absent','Absent')])

    def __str__(self):
        return f"{self.employee.name} - {self.date}"


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.amount}"
