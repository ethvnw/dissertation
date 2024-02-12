from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def index(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')