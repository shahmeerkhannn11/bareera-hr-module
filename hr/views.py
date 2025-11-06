from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Attendance, Payroll
from django.contrib import messages

# Home/Dashboard
from django.db.models import Avg
from .models import Employee

def home(request):
    employees = Employee.objects.count()
    avg_salary = Employee.objects.aggregate(Avg('salary'))['salary__avg'] or 0
    return render(request, 'hr/home.html', {
        'employees': employees,
        'avg_salary': round(avg_salary, 2),
    })

# Employee list
def employee_list(request):
    all_employees = Employee.objects.all()
    return render(request, 'hr/employees.html', {'employees': all_employees})


# Add Employee
def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        department = request.POST.get('department')
        email = request.POST.get('email')
        salary = request.POST.get('salary')
        date_joined = request.POST.get('date_joined')
        Employee.objects.create(
            name=name,
            position=position,
            department=department,
            email=email,
            salary=salary,
            date_joined=date_joined
        )
        messages.success(request, "Employee added successfully!")
        return redirect('employee_list')
    return render(request, 'hr/add_employee.html')

def edit_employee(request, emp_id):
    emp = Employee.objects.get(id=emp_id)
    if request.method == 'POST':
        emp.name = request.POST.get('name')
        emp.position = request.POST.get('position')
        emp.department = request.POST.get('department')
        emp.email = request.POST.get('email')
        emp.salary = request.POST.get('salary')
        emp.date_joined = request.POST.get('date_joined')
        emp.save()
        messages.success(request, "Employee updated successfully!")
        return redirect('employee_list')
    return render(request, 'hr/edit_employee.html', {'emp': emp})


def delete_employee(request, emp_id):
    emp = Employee.objects.get(id=emp_id)
    emp.delete()
    messages.warning(request, "Employee deleted successfully!")
    return redirect('employee_list')

