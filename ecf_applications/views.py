import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory, modelformset_factory
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.formats import date_format
from django.views.generic import DetailView, ListView, TemplateView, View
from formtools.wizard.views import SessionWizardView

from authentication.decorators import secretary_required, staff_required, student_required
from authentication.models import Student, User
from dashboard.models import Notification
from ecf_applications.models import CODES as ECF_CODES
from ecf_applications.models import (ECFApplication, ECFApplicationAssessment,
                                     ECFApplicationAssessmentComment,
                                     ECFApplicationComment)

from .forms import ECFApplicationAssessmentForm, ECFApplicationForm

ECFApplicationAssessmentFormset = formset_factory(
    form=ECFApplicationAssessmentForm, extra=1
)

FORMS = [
    ('application_form', ECFApplicationForm),
    ('assessment_formset', ECFApplicationAssessmentFormset),
]

TEMPLATES = {
    'application_form': 'ecf_applications/new/application_form.html',
    'assessment_formset': 'ecf_applications/new/assessment_form.html'
}


@method_decorator(student_required, name="dispatch")
class NewECFApplicationWizardView(SessionWizardView):
    form_list = FORMS
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["student"] = Student.objects.get(user=self.request.user)
        return context

    def render_goto_step(self, goto_step, **kwargs):
        current_form = self.get_form(self.storage.current_step, data=self.request.POST,files=self.request.FILES)

        if current_form.is_valid():
            self.storage.set_step_data(
                self.storage.current_step, self.process_step(current_form))
            self.storage.set_step_files(
                self.storage.current_step, self.process_step_files(current_form))

            self.storage.current_step = goto_step
            form = self.get_form(
                data=self.storage.get_step_data(self.steps.current),
                files=self.storage.get_step_files(self.steps.current))
            return self.render(form, **kwargs)
        
        else:
            return self.render(current_form, **kwargs)
        
        
    def done(self, form_list, form_dict, **kwargs):
        application = form_dict['application_form']
        application = application.save(commit=False)
        application.applicant = self.request.user
        application.save()

        assessment_formset = form_dict['assessment_formset']
        
        for assessment_form in assessment_formset:
            assessment = assessment_form.save(commit=False)
            assessment.application = application
            assessment.save()

        Notification.objects.bulk_create([
            Notification(
                application=application,
                user=user,
                message="A new ECF application has been submitted"
            )
            for user in User.objects.filter(
                department=self.request.user.department,
                role=User.SECRETARY
            )
        ])
        return redirect('ecf_application:success')


@method_decorator(student_required, name="dispatch")
class ECFApplicationSuccessView(TemplateView):
    template_name = "ecf_applications/new/success.html"


@method_decorator(login_required, name="dispatch")
class ECFApplicationDetailView(DetailView):
    model = ECFApplication
    template_name = "ecf_applications/detail/student_detail.html"
    context_object_name = "application"

    def get(self, request, *args, **kwargs):
        if request.user.role == User.STUDENT:
            if self.get_object().applicant != request.user:
                raise PermissionDenied

            if self.get_object().status == ECF_CODES["ACTION_REQUIRED"]:
                return redirect('ecf_application:edit', pk=self.get_object().pk)
        
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.user.role == User.SECRETARY:
            return "ecf_applications/detail/secretary_detail.html"
        
        elif self.request.user.role == User.SCRUTINY:
            return "ecf_applications/detail/scrutiny_detail.html"
        
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assessments"] = ECFApplicationAssessment.objects.filter(
            application=self.object
        )

        if self.request.user.role == User.SECRETARY or self.request.user.role == User.SCRUTINY:
            context["student"] = Student.objects.get(user=self.object.applicant)
            
            context["application_comments"] = ECFApplicationComment.objects.filter(
                application=self.object
            )
            context["assessment_comments"] = ECFApplicationAssessmentComment.objects.filter(
                assessment__application=self.object
            )

        return context
    
    def post(self, request, *args, **kwargs):
        application = self.get_object()
        evidence = request.FILES.get('evidence')
        application.evidence = evidence
        application.save()

        messages.success(request, "Evidence uploaded successfully")
        return redirect('ecf_application:detail', pk=application.pk)
        

@method_decorator(secretary_required, name="dispatch")
class EvidenceReminderView(View):
    def post(self, request, *args, **kwargs):
        application = ECFApplication.objects.get(pk=kwargs['pk'])
        
        date = date_format(application.submission_date, "d F Y")
        Notification.objects.create(
            application=application,
            user=application.applicant,
            message=f"Please upload evidence for your {date} application"
        )
        messages.success(request, "Reminder sent successfully")

        return redirect('ecf_application:detail', pk=application.pk)


@method_decorator(secretary_required, name="dispatch")
class CommentSendView(View):
    def post(self, request, *args, **kwargs):
        application = ECFApplication.objects.get(pk=kwargs['pk'])
        application.status = ECF_CODES['ACTION_REQUIRED']
        application.save()

        for key in request.POST:
            if key.startswith('application'):
               ECFApplicationComment.objects.create(
                   application=application,
                   user=request.user,
                   comment=request.POST[key]
               )

            elif key.startswith('assessment'):
                ECFApplicationAssessmentComment.objects.create(
                    assessment=ECFApplicationAssessment.objects.get(pk=key.split('-')[1]),
                    user=request.user,
                    comment=request.POST[key]
                )

        date = date_format(application.submission_date, "d F Y")
        Notification.objects.create(
            application=application,
            user=application.applicant,
            message=f"Your {date} application has new comments"
        )
        messages.success(request, "Comments sent successfully")

        return redirect('ecf_application:detail', pk=application.pk)
    

@method_decorator(student_required, name="dispatch")
class ECFApplicationEditView(TemplateView):
    template_name = "ecf_applications/edit.html"

    def get(self, request, *args, **kwargs):
        application = get_object_or_404(ECFApplication, pk=kwargs['pk'])

        if application.applicant != request.user:
            raise PermissionDenied

        if application.status != ECF_CODES["ACTION_REQUIRED"]:
            messages.error(request, "You cannot edit this application")
            return redirect('ecf_application:detail', pk=application.pk)

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = ECFApplication.objects.get(pk=kwargs['pk'])

        application_comments = ECFApplicationComment.objects.filter(
            application=self.kwargs['pk'])
        
        if application_comments:
            context["application_comments"] = application_comments
            context["application_form"] = ECFApplicationForm(instance=context["application"], prefix="application_form")


        assessment_comments = ECFApplicationAssessmentComment.objects.filter(
            assessment__application=self.kwargs['pk'])
        
        if assessment_comments:
            assessments = ECFApplicationAssessment.objects.filter(
                pk__in=[comment.assessment.pk for comment in assessment_comments]
            )
            context["assessments"] = assessments

            assessment_comments_dict = {}
            for comment in assessment_comments:
                if comment.assessment.pk in assessment_comments_dict:
                    assessment_comments_dict[comment.assessment.pk].append(comment)
                else:
                    assessment_comments_dict[comment.assessment.pk] = [comment]

            context["assessment_comments_dict"] = assessment_comments_dict

            assessment_formset = modelformset_factory(
                ECFApplicationAssessment, form=ECFApplicationAssessmentForm, extra=0
            )
            context["assessment_formset"] = assessment_formset(queryset=assessments)

        return context 
    

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if "application_form" in context:
            application_form = ECFApplicationForm(
                request.POST, request.FILES, instance=context["application"], prefix="application_form"
            )

            if not application_form.is_valid():
                context["application_form"] = application_form
                return self.render_to_response(context)
            
            application = application_form.save(commit=False)
            application.status = ECF_CODES["PENDING"]
            application.save()

        if "assessment_formset" in context:
            assessment_formset = modelformset_factory(
                ECFApplicationAssessment, form=ECFApplicationAssessmentForm, extra=0
            )(request.POST, queryset=context["assessments"])

            if not assessment_formset.is_valid():
                context["assessment_formset"] = assessment_formset
                return self.render_to_response(context)
            
            assessment_formset.save()

        if not "application_form" in context:
            application = context["application"]
            application.status = ECF_CODES["PENDING"]
            application.save()
            
        Notification.objects.bulk_create([
            Notification(
                application=application,
                user=user,
                message=f"{application.applicant} has edited their ECF application"
            )
            for user in User.objects.filter(
                department=request.user.department,
                role=User.SECRETARY
            )
        ])
        return redirect('ecf_application:detail', pk=context["application"].pk)


@method_decorator(staff_required, name="dispatch")
class ECFApplicationListView(ListView):
    model = ECFApplication
    template_name = "ecf_applications/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        applications = ECFApplication.objects.filter(
            applicant__department=self.request.user.department
        ).order_by("-last_modified")

        finalised_applications = applications.filter(status__in=[
            ECF_CODES["APPROVED"], ECF_CODES["REJECTED"], ECF_CODES["PARTIAL_APPROVAL"]
        ])

        context["finalised_applications"] = finalised_applications

        context["ongoing_applications"] = applications.exclude(
            pk__in=finalised_applications
        )

        return context


@method_decorator(secretary_required, name="dispatch")
class ECFApplicationDecisionView(TemplateView):
    template_name = "ecf_applications/decision.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = ECFApplication.objects.get(pk=self.kwargs['pk'])
        context["assessments"] = ECFApplicationAssessment.objects.filter(
            application=context["application"]
        )
                
        context["application_comments"] = ECFApplicationComment.objects.filter(
            application=context["application"]
        )
        context["assessment_comments"] = ECFApplicationAssessmentComment.objects.filter(
            assessment__application=context["application"]
        )

        return context
    
    def post(self, request, *args, **kwargs):
        application = ECFApplication.objects.get(pk=kwargs['pk'])
        assessments = ECFApplicationAssessment.objects.filter(application=application)

        for assessment in assessments:
            decision = request.POST.get(f'{assessment.pk}-decision')
            
            if decision == "approve":
                assessment.status = ECF_CODES['APPROVED']
            elif decision == "reject":
                assessment.status = ECF_CODES['REJECTED']

            if decision:
                assessment.save()

        # set application status to approved if all assessments are approved
        if all([assessment.status == ECF_CODES['APPROVED'] for assessment in assessments]):
            application.status = ECF_CODES['APPROVED']
        elif all([assessment.status == ECF_CODES['REJECTED'] for assessment in assessments]):
            application.status = ECF_CODES['REJECTED']
        else:
            application.status = ECF_CODES['PARTIAL_APPROVAL']

        application.save()

        messages.success(request, "Decision submitted successfully")
        Notification.objects.create(
            application=application,
            user=application.applicant,
            message="A decision has been made on your ECF application"
        )
        return redirect('ecf_application:detail', pk=application.pk)

