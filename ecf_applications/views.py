import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View
from formtools.wizard.views import SessionWizardView

from authentication.decorators import secretary_required, student_required
from authentication.models import Student, User
from ecf_applications.models import CODES as ECF_CODES
from ecf_applications.models import ECFApplication, ECFApplicationAssessment, ECFApplicationComment, ECFApplicationAssessmentComment

from .forms import ECFApplicationAssessmentForm, ECFApplicationForm

ECFApplicationAssessmentFormset = formset_factory(
    form=ECFApplicationAssessmentForm, extra=1
)

FORMS = [
    ('application_form', ECFApplicationForm),
    ('assessment_formset', ECFApplicationAssessmentFormset),
]

TEMPLATES = {
    'application_form': 'ecf_applications/application_form.html',
    'assessment_formset': 'ecf_applications/assessment_form.html'
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

        return redirect('ecf_application:success')


@method_decorator(student_required, name="dispatch")
class ECFApplicationSuccessView(TemplateView):
    template_name = "ecf_applications/success.html"


@method_decorator(login_required, name="dispatch")
class ECFApplicationDetailView(DetailView):
    model = ECFApplication
    template_name = "ecf_applications/detail.html"
    context_object_name = "application"

    def get_template_names(self):
        if self.request.user.role == User.SECRETARY:
            return "ecf_applications/secretary_detail.html"
        
        elif self.request.user.role == User.SCRUTINY:
            return "ecf_applications/scrutiny_detail.html"
        
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assessments"] = ECFApplicationAssessment.objects.filter(
            application=self.object
        )

        if self.request.user.role == User.SECRETARY:
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
class CommentSendView(View):
    def post(self, request, *args, **kwargs):
        application = ECFApplication.objects.get(pk=kwargs['pk'])
        

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

        messages.success(request, "Comments sent successfully")

        return redirect('ecf_application:detail', pk=application.pk)