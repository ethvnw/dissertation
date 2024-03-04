from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from accounts.forms import StudentUpdateForm
from accounts.models import Student
from ecfapps.models import ECFApplication


def index(request):
    return redirect('dashboard')

@login_required
def profile(request):
    if request.method == 'POST':
        support_form = StudentUpdateForm(request.POST, request.FILES)

        if support_form.is_valid():
            student = Student.objects.get(user=request.user)
            student.support_plan = support_form.cleaned_data['support_plan']
            student.save()
            
            return redirect('profile')
        
    else:
        support_form = StudentUpdateForm()
        return render(request, 'dashboard/profile.html', {
            'support_form': support_form,
        })

@login_required
def dashboard(request):
    if request.user.is_staff:
        ecf_apps = ECFApplication.objects.filter(
            student__department__contains=request.user.department
        ).order_by('-submission_date')

        return render(request, 'dashboard/staff_dashboard.html', {'ecf_apps': ecf_apps})
    
    else:
        ecf_apps = ECFApplication.objects.filter(student=request.user).order_by('-submission_date')
        
        return render(request, 'dashboard/student_dashboard.html', {'ecf_apps': ecf_apps})