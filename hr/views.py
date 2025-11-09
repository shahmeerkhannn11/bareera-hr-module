from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.http import HttpResponse
from django.contrib import messages
import csv
from .models import Employee, Attendance, Payroll


# ---------------------------
# HOME / DASHBOARD
# ---------------------------
def home(request):
    employee_count = Employee.objects.count()
    attendance_count = Attendance.objects.count()
    payroll_count = Payroll.objects.count()
    average_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    return render(request, 'hr/home.html', {
        'employee_count': employee_count,
        'attendance_count': attendance_count,
        'payroll_count': payroll_count,
        'average_salary': round(average_salary, 2),
    })


# ---------------------------
# EMPLOYEE CRUD
# ---------------------------
def employee_list(request):
    q = request.GET.get('q', '')
    employees = Employee.objects.filter(name__icontains=q)
    return render(request, 'hr/employees.html', {'employees': employees, 'query': q})


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
        messages.success(request, "✅ Employee added successfully!")
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
        messages.success(request, "✏️ Employee details updated successfully!")
        return redirect('employee_list')
    return render(request, 'hr/edit_employee.html', {'employee': employee})

def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    employee.delete()
    messages.success(request, "🗑️ Employee deleted successfully.")
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
    writer.writerow(['Name', 'Position', 'Department', 'Email', 'Salary'])
    for emp in Employee.objects.all():
        writer.writerow([emp.name, emp.position, emp.department, emp.email, emp.salary])
    return response
