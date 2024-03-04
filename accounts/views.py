from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django_sendfile import sendfile
from django.core.exceptions import PermissionDenied

from ecfapps.models import ECFApplication
from .models import Student
from .forms import CustomUserCreationForm, StudentCreationForm, UserLoginForm


@login_required
def download(request):
    file_name = request.GET.get('file')
    file_type = file_name.split('/')[0]
    
    if file_type == 'evidence':
        application = get_object_or_404(ECFApplication, evidence=file_name)
        
        if application.student != request.user:
            raise PermissionDenied()
        
    elif file_type == 'support_plans':
        student = get_object_or_404(Student, support_plan=file_name)
        
        if student.user != request.user:
            raise PermissionDenied()
        
    return sendfile(request, file_name)


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentCreationForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)

            student.user = user
            student.save()

            return redirect('login')

    else:
        user_form = CustomUserCreationForm()
        student_form = StudentCreationForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form, 'student_form': student_form
    })


def login(request):
    if request.user.is_authenticated:
        return redirect('student:dashboard')
    
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)

        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                user_form.add_error(None, "Email or password is incorrect")
    else:
        user_form = UserLoginForm()

    return render(request, 'accounts/login.html', {'user_form': user_form})


def logout(request):
    auth_logout(request)
    return redirect('login')
