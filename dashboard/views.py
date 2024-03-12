from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import UpdateView
from django_sendfile import sendfile

from authentication.decorators import student_required
from authentication.models import Student, User
from ecf_applications.models import CODES as ECF_CODES
from ecf_applications.models import ECFApplication

from .forms import ProfileForm, StudentProfileForm


@login_required
def index(request):
    return redirect("dashboard")
    
    
@method_decorator(login_required, name="dispatch")
class DownloadView(View):
    def post(self, request):
        file_name = request.POST.get('file')
        file_type = file_name.split('/')[0]

        if file_type == 'evidence':
            application = get_object_or_404(ECFApplication, evidence=file_name)

            if application.applicant != request.user and not (
                request.user.role == User.SCRUTINY or request.user.role == User.SECRETARY):
                raise PermissionDenied()

        elif file_type == 'support_plans':
            student = get_object_or_404(Student, support_plan=file_name)

            if student.user != request.user and not (
                request.user.role == User.SCRUTINY or request.user.role == User.SECRETARY):
                raise PermissionDenied()
            
        return sendfile(request, file_name, attachment=True)


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_template_names(self):
        if self.request.user.role == User.SECRETARY:
            return "dashboard/secretary_dashboard.html"
        
        elif self.request.user.role == User.SCRUTINY:
            return "dashboard/scrutiny_dashboard.html"
        
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.role == User.SECRETARY:
            context["ecf_apps"] = ECFApplication.objects.filter(
                status=ECF_CODES["PENDING"],
                applicant__department=self.request.user.department
            ).order_by("-last_modified")
        
        elif self.request.user.role == User.SCRUTINY:
            context["ecf_apps"] = ECFApplication.objects.filter(
                status=ECF_CODES["UNDER_REVIEW"],
                applicant__department=self.request.user.department
            ).order_by("-last_modified")
            
        else:
            context["ecf_apps"] = ECFApplication.objects.filter(
                applicant=self.request.user).order_by("-last_modified")
        
        return context    


@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    model = User
    template_name = "dashboard/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user)

        if self.request.user.role == User.STUDENT:
            student = Student.objects.get(user=self.request.user)
            context["student"] = student
            context["student_form"] = StudentProfileForm(instance=student)

        return context
    
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)

        if request.user.role == User.STUDENT:
            student_form = StudentProfileForm(request.POST, request.FILES, instance=Student.objects.get(user=request.user))
            
            if form.is_valid() and student_form.is_valid():
                form.save()
                student_form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profile")
        
        else:
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profile")
        
        return render(request, "dashboard/profile.html", {"form": form})
