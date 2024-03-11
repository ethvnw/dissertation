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

from .forms import StaffProfileForm, StudentProfileForm


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
            ).order_by("-submission_date")
        
        elif self.request.user.role == User.SCRUTINY:
            context["ecf_apps"] = ECFApplication.objects.filter(
                status=ECF_CODES["UNDER_REVIEW"],
                applicant__department=self.request.user.department
            ).order_by("-submission_date")
            
        else:
            context["ecf_apps"] = ECFApplication.objects.filter(
                applicant=self.request.user).order_by("-submission_date")
        
        return context
    

@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    form_class = StudentProfileForm
    template_name = "dashboard/student_profile.html"
    model = User

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            raise PermissionDenied()
        
        if not request.user.role == User.STUDENT:
            self.form_class = StaffProfileForm
        
        return super().get(request, *args, **kwargs)
    
    def get_template_names(self):
            if not self.request.user.role == User.STUDENT:
                return "dashboard/profile.html"
            
            return self.template_name

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully")
        return reverse("profile", kwargs={"pk": self.get_object().pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.role == User.STUDENT:
            context["form"] = StaffProfileForm(instance=self.get_object())
            return context

        student = Student.objects.get(user=self.get_object())
        context["student"] = student
        context["form"] = StudentProfileForm(
            instance=self.get_object(),
            initial={
                "study_level": student.study_level,
                "course": student.course,
                "support_plan": student.support_plan
            }
        )

        return context
    
    def form_valid(self, form):
        student = Student.objects.get(user=self.get_object())
        student.study_level = form.cleaned_data["study_level"]
        student.course = form.cleaned_data["course"]

        if form.cleaned_data["support_plan"]:
            student.support_plan = form.cleaned_data["support_plan"]
            
        student.save()

        return super().form_valid(form)
    