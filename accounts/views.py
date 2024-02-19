from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login

from .forms import CustomUserCreationForm, StudentCreationForm, UserLoginForm

# Create your views here.

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
        return redirect('dashboard')
    
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
