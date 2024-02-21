from django import forms

from .models import ECFApplication, ECFApplicationModuleAssessment

class ECFApplicationForm(forms.ModelForm):
    template_name = "ecfapps/form.html"

    circumstance = forms.ChoiceField(
        label="What is the nature of your extenuating circumstances?",
        choices=ECFApplication.CIRCUMSTANCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',}))
    
    start_date = forms.DateField(
        label='What is the approximate start date of your circumstances?',
        widget=forms.DateInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'type': 'date'}))
    
    ongoing = forms.ChoiceField(
        required=False,
        label='Are your circumstances ongoing?',
        widget=forms.RadioSelect(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 felx'}
        ),
        choices=((True, 'Yes'), (False, 'No')))

    end_date = forms.DateField(
        required=False,
        label='What is the approximate end date of your circumstances?',
        widget=forms.DateInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'type': 'date'}))
    
    description = forms.CharField(
        label='Please provide a summary of your circumstances, including the impact on you and your studies.',
        widget=forms.Textarea(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Your answer'}))
    
    evidence = forms.FileField(
        required=False,
        label='Upload your evidence (can also be submitted later)',
        widget=forms.FileInput(attrs={
            'class': 'mb-2',
            'placeholder': 'Evidence'}))
    
    class Meta:
        model = ECFApplication
        fields = ('circumstance', 'start_date', 'ongoing', 'end_date', 'description', 'evidence')


class ECFApplicationModuleAssessmentForm(forms.ModelForm):
    template_name = "ecfapps/form.html"

    module_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Code for the affected module'}))
    
    assessment = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Name of the affected assessment'}))
    
    action = forms.ChoiceField(
        label="What action are you requesting?",
        choices=ECFApplicationModuleAssessment.ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',}))
    
    extension_date = forms.DateField(
        required=False,
        label='If you are requesting an extension, what is the new deadline?',
        widget=forms.DateInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'type': 'date'}))
    
    more_info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'More information'}))
                                     
    class Meta:
        model = ECFApplicationModuleAssessment
        fields = ('module_code', 'assessment', 'action', 'extension_date', 'more_info')

    
ECFApplicationModuleAssessmentFormSet = forms.modelformset_factory(
    ECFApplicationModuleAssessment,
    form=ECFApplicationModuleAssessmentForm,
    extra=1
)
