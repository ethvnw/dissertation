from django import forms

from .models import ECFApplication, ECFApplicationModuleAssessment

class ECFApplicationForm(forms.ModelForm):
    circumstance = forms.ChoiceField(
        label="What is the nature of your extenuating circumstances?",
        choices=ECFApplication.CIRCUMSTANCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',}))
    
    start_date = forms.DateField(
        label='What is the approximate start date of your circumstances?',
        widget=forms.DateInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',
            'type': 'date'}))
    
    ongoing = forms.ChoiceField(
        label='Are your circumstances ongoing?',
        widget=forms.RadioSelect(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 felx'}
        ),
        choices=((True, 'Yes'), (False, 'No')))

    end_date = forms.DateField(
        required=False,
        label='What is the approximate end date of your circumstances?',
        widget=forms.DateInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',
            'type': 'date'}))
    
    description = forms.CharField(
        label='Please provide a summary of your circumstances, including the impact on you and your studies.',
        widget=forms.Textarea(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',
            'placeholder': 'Your answer'}))
    
    evidence = forms.FileField(
        required=False,
        label='Upload your evidence (can also be submitted later)',
        widget=forms.FileInput(attrs={
            'class': 'mb-4',
            'placeholder': 'Evidence'}))
    
    class Meta:
        model = ECFApplication
        fields = ('circumstance', 'start_date', 'ongoing', 'end_date', 'description', 'evidence')


class ECFApplicationModuleAssessmentForm(forms.ModelForm):
    module_code = forms.CharField(
        label='What is the module code for the affected assessment?',
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',
            'placeholder': 'ABC1234'}))
    
    assessment = forms.CharField(
        label='What is the name of the affected assessment?',
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',
            'placeholder': 'Assignment one'}))
    
    action = forms.ChoiceField(
        label="What action are you requesting?",
        choices=ECFApplicationModuleAssessment.ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',}))
    
    extension_date = forms.DateField(
        required=False,
        label='What is your proposed new submission date?',
        widget=forms.DateInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',
            'type': 'date'}))
    
    more_info = forms.CharField(
        required=False,
        label='Do you have any more information to add (optional)?',
        widget=forms.Textarea(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-4 w-full',
            'placeholder': 'Your answer'}))
                                     
    class Meta:
        model = ECFApplicationModuleAssessment
        fields = ('module_code', 'assessment', 'action', 'extension_date', 'more_info')
