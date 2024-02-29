import os
from django.forms import formset_factory
from django.conf import settings
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from formtools.wizard.views import SessionWizardView

from .forms import ECFApplicationForm, ECFApplicationModuleAssessmentForm

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
        print(application_form.cleaned_data)
        application = application_form.save(commit=False)
        application.student = self.request.user
        application.save()

        module_formset = form_dict['module_formset']
        for form in module_formset:
            assessment = form.save(commit=False)
            assessment.application = application
            assessment.save()
        
        return redirect('ecfapps:success')


def success(request):
    return render(request, 'ecfapps/success.html')
