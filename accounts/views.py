from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout

from .forms import CustomUserCreationForm, StudentCreationForm

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

    return render(request, 'register.html', {
        'user_form': user_form, 'student_form': student_form
    })


def logout(request):
    auth_logout(request)
    return redirect('login')
