from django.shortcuts import redirect, render

from .forms import ECFApplicationForm, ECFApplicationModuleAssessmentForm

def new(request):
    if request.method == 'POST':
        app_form = ECFApplicationForm(request.POST, request.FILES)
        assessment_form = ECFApplicationModuleAssessmentForm(request.POST)

        if app_form.is_valid() and assessment_form.is_valid():
            app = app_form.save(commit=False)
            assessment = assessment_form.save(commit=False)

            app.student = request.user
            app.save()

            assessment.application = app
            assessment.save()

            return redirect('dashboard')
        
    else:
        app_form = ECFApplicationForm()
        assessment_form = ECFApplicationModuleAssessmentForm()

    return render(request, 'ecfapps/new.html', {
        'app_form': app_form, 'assessment_form': assessment_form
    })
