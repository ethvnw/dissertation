from django import forms
from django.utils import timezone

from .models import ECFApplication, ECFApplicationAssessment


class ECFApplicationForm(forms.ModelForm):
    template_name = "ecf_applications/form.html"

    def __init__(self, *args, **kwargs):
        super(ECFApplicationForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if visible.field.widget.__class__.__name__ == "RadioSelect":
                visible.field.widget.attrs['class'] = 'mb-2'
            else:
                visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'

    circumstance = forms.ChoiceField(
        choices=[("", "Select from the list")] + ECFApplication.CIRCUMSTANCE_CHOICES,
        label="What is the nature of your circumstances?",
        required=True,
    )

    start_date = forms.DateField(
        label="What is the start date of your circumstances?",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    end_date = forms.DateField(
        label="What is the end date of your circumstances?",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    ongoing = forms.ChoiceField(
        label="Are your circumstances ongoing?",
        widget=forms.RadioSelect(
            attrs={"class": "w-2"}),
        choices=[(True, "Yes"), (False, "No")]
    )

    description = forms.CharField(
        label="Please provide a brief description of your circumstances",
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Your answer'})
    )

    evidence = forms.FileField(
        label="Please upload evidence (may also be submitted at a later date)",
        required=False,
        widget=forms.FileInput()
    )


    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        if start_date and start_date > timezone.localdate():
            raise forms.ValidationError("Start date cannot be in the future.")
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be after start date.")
        return end_date

    class Meta:
        model = ECFApplication
        fields = ("circumstance", "start_date", "ongoing", "end_date", "description", "evidence")



class ECFApplicationAssessmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ECFApplicationAssessmentForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'

    module = forms.CharField(
        label="Code of the Affected Module",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. ABC123'})
    )

    assessment = forms.CharField(
        label="Name of the Affected Assessment",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Assignment 1'})
    )

    action = forms.ChoiceField(
        choices=[("", "Select from the list")] + ECFApplicationAssessment.ACTION_CHOICES,
        label="What action do you propose?",
    )

    extension_date = forms.DateField(
        label="What is the new due date?",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = ECFApplicationAssessment
        fields = ("module", "assessment", "action", "extension_date", "description")
