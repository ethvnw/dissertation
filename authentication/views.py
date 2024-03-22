from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import StudentSignInForm, StudentSignUpForm
from .models import User


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'authentication/registration/student_signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        
        return redirect('dashboard')
    

class StudentSignInView(auth_views.LoginView):
    template_name = 'authentication/login/student_signin.html'
    authentication_form = StudentSignInForm


def signout(request):
    auth_logout(request)
    messages.success(request, "You have been signed out.")
    return redirect('signin')