from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.http import HttpResponse
import csv
from .models import Employee, Attendance, Payroll


# ---------------------------
# HOME / DASHBOARD
# ---------------------------
def home(request):
    total_employees = Employee.objects.count()
    avg_salary = Employee.objects.aggregate(Avg('salary'))['salary__avg'] or 0
    total_attendance = Attendance.objects.count()
    total_payroll = Payroll.objects.count()

    context = {
        'total_employees': total_employees,
        'avg_salary': round(avg_salary, 2),
        'total_attendance': total_attendance,
        'total_payroll': total_payroll,
    }
    return render(request, 'hr/home.html', context)


# ---------------------------
# EMPLOYEE CRUD
# ---------------------------
def employee_list(request):
    employees = Employee.objects.all().order_by('emp_id')
    return render(request, 'hr/employees.html', {'employees': employees})


def add_employee(request):
    if request.method == 'POST':
        Employee.objects.create(
            name=request.POST.get('name'),
            position=request.POST.get('position'),
            department=request.POST.get('department'),
            email=request.POST.get('email'),
            salary=request.POST.get('salary'),
            date_joined=request.POST.get('date_joined')
        )
        return redirect('employee_list')
    return render(request, 'hr/add_employee.html')


def edit_employee(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.position = request.POST.get('position')
        employee.department = request.POST.get('department')
        employee.email = request.POST.get('email')
        employee.salary = request.POST.get('salary')
        employee.date_joined = request.POST.get('date_joined')
        employee.save()
        return redirect('employee_list')
    return render(request, 'hr/edit_employee.html', {'employee': employee})


def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    employee.delete()
    return redirect('employee_list')


# ---------------------------
# ATTENDANCE
# ---------------------------
def attendance_list(request):
    attendance = Attendance.objects.select_related('employee').all().order_by('-date')
    return render(request, 'hr/attendance.html', {'attendance': attendance})


# ---------------------------
# PAYROLL
# ---------------------------
def payroll_list(request):
    payroll = Payroll.objects.select_related('employee').all().order_by('-payment_date')
    return render(request, 'hr/payroll.html', {'payroll': payroll})


# ---------------------------
# EXPORT EMPLOYEES (CSV)
# ---------------------------
def export_employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Position', 'Department', 'Email', 'Salary', 'Date Joined'])

    for emp in Employee.objects.all():
        writer.writerow([emp.emp_id, emp.name, emp.position, emp.department, emp.email, emp.salary, emp.date_joined])

    return response
