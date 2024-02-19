from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from ecfapps.models import ECFApplication


def index(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    ecf_apps = ECFApplication.objects.filter(student=request.user)

    return render(request, 'student_dashboard/dashboard.html', {'ecf_apps': ecf_apps})