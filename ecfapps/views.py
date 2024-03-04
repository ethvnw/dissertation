import os
from django.forms import formset_factory
from django.conf import settings
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import FileSystemStorage
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.decorators import login_required

from .models import ECFApplication
from .forms import ECFApplicationEvidenceForm, ECFApplicationForm, ECFApplicationModuleAssessmentForm

ECFApplicationModuleAssessmentFormSet = formset_factory(
    form=ECFApplicationModuleAssessmentForm, extra=1
)

FORMS = [
    ('application_form', ECFApplicationForm),
    ('module_formset', ECFApplicationModuleAssessmentFormSet)
]

TEMPLATES = {
    'application_form': 'ecfapps/application_form.html',
    'module_formset': 'ecfapps/module_form.html'
}

class ECFAppWizard(SessionWizardView):
    form_list = FORMS
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def render_goto_step(self, goto_step, **kwargs):
        print(self.request.FILES)
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
        application_form = form_dict['application_form']
        application = application_form.save(commit=False)
        application.student = self.request.user
        application.save()

        module_formset = form_dict['module_formset']
        for form in module_formset:
            assessment = form.save(commit=False)
            assessment.application = application
            assessment.save()
        
        return redirect('ecfapps:success')


@login_required
def success(request):
    return render(request, 'ecfapps/success.html')


@login_required
def detail(request, pk):
    if request.method == 'POST':
        evidence_form = ECFApplicationEvidenceForm(request.POST, request.FILES)

        if evidence_form.is_valid():
            application = ECFApplication.objects.get(pk=pk)
            application.evidence = evidence_form.cleaned_data['evidence']
            application.save()
            
            return redirect('ecfapps:detail', pk=pk)
        
    else:
        application = get_object_or_404(ECFApplication, pk=pk)

        # only render the page if the user is the owner of the application
        if application.student != request.user:
            raise PermissionDenied()
        
        evidence_form = ECFApplicationEvidenceForm()
        assesssments = application.ecfapplicationmoduleassessment_set.all()

        return render(request, 'ecfapps/detail.html', {
            'application': application,
            'assessments': assesssments, 
            'evidence_form': evidence_form
        })
