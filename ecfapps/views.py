from django.shortcuts import redirect, render

from .models import ECFApplicationModuleAssessment
from .forms import ECFApplicationForm, ECFApplicationModuleAssessmentFormSet

def new(request):
    if request.method == 'POST':
        app_form = ECFApplicationForm(request.POST, request.FILES)
        assessment_formset = ECFApplicationModuleAssessmentFormSet(data=request.POST)

        if app_form.is_valid() and assessment_formset.is_valid():
            app = app_form.save(commit=False)
            assessments = assessment_formset.save(commit=False)

            app.student = request.user
            app.save()

            for assessment in assessments:
                assessment.application = app
                assessment.save()

            return redirect('dashboard')
        
    else:
        app_form = ECFApplicationForm()
        assessment_formset = ECFApplicationModuleAssessmentFormSet(queryset=ECFApplicationModuleAssessment.objects.none())

    return render(request, 'ecfapps/new.html', {
        'app_form': app_form, 'assessment_formset': assessment_formset
    })
