import os
import django
import random
from datetime import date, timedelta

# --- Setup Django environment ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bareera_hr.settings')
django.setup()

from hr.models import Employee, Attendance, Payroll

# --- Clear existing data (optional) ---
Employee.objects.all().delete()
Attendance.objects.all().delete()
Payroll.objects.all().delete()

# --- Create sample Employees ---
employees_data = [
    {"name": "Ali Khan", "position": "HR Manager", "department": "HR", "email": "ali.khan@example.com", "salary": 85000, "date_joined": "2023-02-15"},
    {"name": "Ayesha Malik", "position": "Software Engineer", "department": "IT", "email": "ayesha.malik@example.com", "salary": 120000, "date_joined": "2022-09-10"},
    {"name": "Bilal Ahmed", "position": "Accountant", "department": "Finance", "email": "bilal.ahmed@example.com", "salary": 95000, "date_joined": "2023-01-05"},
    {"name": "Sara Iqbal", "position": "HR Assistant", "department": "HR", "email": "sara.iqbal@example.com", "salary": 70000, "date_joined": "2023-03-20"},
    {"name": "Usman Tariq", "position": "Team Lead", "department": "IT", "email": "usman.tariq@example.com", "salary": 135000, "date_joined": "2021-07-01"},
]

employees = []
for e in employees_data:
    emp = Employee.objects.create(**e)
    employees.append(emp)

print(f"✅ Added {len(employees)} employees successfully.")

# --- Create random Attendance records for last 7 days ---
statuses = ['Present', 'Absent']
for emp in employees:
    for i in range(7):
        Attendance.objects.create(
            employee=emp,
            date=date.today() - timedelta(days=i),
            status=random.choice(statuses)
        )

print("✅ Added attendance records for last 7 days.")

# --- Create Payroll entries ---
for emp in employees:
    Payroll.objects.create(
        employee=emp,
        payment_date=date.today(),
        amount=emp.salary,
        remarks="Monthly Salary"
    )

print("✅ Added payroll records successfully.")
print("🎉 Database populated! Now open your app to view sample data.")
