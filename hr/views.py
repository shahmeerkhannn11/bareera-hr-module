from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import date
import csv

from .models import Employee, EmployeeProfile, Attendance, Payroll


# -------------------------------------------------------
# ROLE CHECKERS
# -------------------------------------------------------
def is_admin(user):
    return user.is_superuser

def is_employee(user):
    return hasattr(user, "employee_profile")


# -------------------------------------------------------
# SIGNUP – Employee Self Registration
# -------------------------------------------------------
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        position = request.POST.get("position")
        department = request.POST.get("department")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        emp = Employee.objects.create(
            name=username,
            position=position,
            department=department,
            email=email,
            salary=0,
            date_joined=date.today(),
        )

        EmployeeProfile.objects.create(user=user, employee=emp)

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "hr/signup.html")


# -------------------------------------------------------
# LOGIN
# -------------------------------------------------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect("home")
            elif is_employee(user):
                return redirect("employee_dashboard")
            else:
                messages.error(request, "No role assigned!")
                return redirect("login")

        messages.error(request, "Invalid username or password.")

    return render(request, "hr/login.html")


# -------------------------------------------------------
# LOGOUT
# -------------------------------------------------------
def user_logout(request):
    logout(request)
    return redirect("login")


# -------------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def home(request):
    return render(request, "hr/home.html", {
        "employee_count": Employee.objects.count(),
        "attendance_count": Attendance.objects.count(),
        "payroll_count": Payroll.objects.count(),
        "average_salary": round(
            Employee.objects.aggregate(avg_salary=Avg("salary"))["avg_salary"] or 0, 
            2
        ),
    })


# -------------------------------------------------------
# EMPLOYEE DASHBOARD
# -------------------------------------------------------
@login_required
@user_passes_test(is_employee)
def employee_dashboard(request):
    emp = request.user.employee_profile.employee
    return render(request, "hr/employee_dashboard.html", {
        "employee": emp,
        "attendance": Attendance.objects.filter(employee=emp),
        "payroll": Payroll.objects.filter(employee=emp),
    })


# -------------------------------------------------------
# EMPLOYEE CRUD
# -------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def employee_list(request):
    query = request.GET.get("q", "")
    employees = Employee.objects.filter(name__icontains=query)
    return render(request, "hr/employees.html", {
        "employees": employees,
        "query": query
    })


@login_required
@user_passes_test(is_admin)
def add_employee(request):
    if request.method == "POST":
        Employee.objects.create(
            name=request.POST["name"],
            position=request.POST["position"],
            department=request.POST["department"],
            email=request.POST["email"],
            salary=request.POST["salary"],
            date_joined=request.POST["date_joined"],
        )
        messages.success(request, "Employee added successfully!")
        return redirect("employee_list")

    return render(request, "hr/add_employee.html")


@login_required
@user_passes_test(is_admin)
def edit_employee(request, emp_id):
    emp = get_object_or_404(Employee, emp_id=emp_id)

    if request.method == "POST":
        emp.name = request.POST["name"]
        emp.position = request.POST["position"]
        emp.department = request.POST["department"]
        emp.email = request.POST["email"]
        emp.salary = request.POST["salary"]
        emp.date_joined = request.POST["date_joined"]
        emp.save()

        messages.success(request, "Employee updated!")
        return redirect("employee_list")

    return render(request, "hr/edit_employee.html", {"employee": emp})


@login_required
@user_passes_test(is_admin)
def delete_employee(request, emp_id):
    get_object_or_404(Employee, emp_id=emp_id).delete()
    messages.success(request, "Employee deleted.")
    return redirect("employee_list")


# -------------------------------------------------------
# ATTENDANCE (LIST + CREATE)
# -------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def attendance_list(request):
    attendance = Attendance.objects.select_related("employee")
    return render(request, "hr/attendance.html", {"attendance": attendance})


@login_required
@user_passes_test(is_admin)
def add_attendance(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        Attendance.objects.create(
            employee_id=request.POST.get("employee"),
            status=request.POST.get("status"),
            date=request.POST.get("date")
        )

        messages.success(request, "Attendance added successfully!")
        return redirect("attendance_list")

    return render(request, "hr/add_attendance.html", {"employees": employees})


# -------------------------------------------------------
# PAYROLL (LIST + CREATE)
# -------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def payroll_list(request):
    payroll = Payroll.objects.select_related("employee")
    return render(request, "hr/payroll.html", {"payroll": payroll})


@login_required
@user_passes_test(is_admin)
def add_payroll(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        Payroll.objects.create(
            employee_id=request.POST.get("employee"),
            amount=request.POST.get("amount"),
            remarks=request.POST.get("remarks"),
            payment_date=request.POST.get("payment_date")
        )

        messages.success(request, "Payroll record added successfully!")
        return redirect("payroll_list")

    return render(request, "hr/add_payroll.html", {"employees": employees})


# -------------------------------------------------------
# EXPORT CSV
# -------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def export_employees_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=employees.csv"

    writer = csv.writer(response)
    writer.writerow(["Name", "Position", "Department", "Email", "Salary"])

    for emp in Employee.objects.all():
        writer.writerow([
            emp.name,
            emp.position,
            emp.department,
            emp.email,
            emp.salary
        ])

    return response
