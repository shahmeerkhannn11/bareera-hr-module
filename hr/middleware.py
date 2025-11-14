from django.shortcuts import redirect
from django.urls import reverse

class PreventEmployeeFromAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # if user is logged in but NOT superuser, block /admin/
        if request.path.startswith('/admin/'):
            if request.user.is_authenticated and not request.user.is_superuser:
                return redirect('employee_dashboard')

        return self.get_response(request)
