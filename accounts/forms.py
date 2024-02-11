from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from .models import CustomUser, Student


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.label = ""

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@sheffield.ac.uk" not in data:
            raise forms.ValidationError("Must be a valid sheffield.ac.uk address")
        
        return data

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email (@sheffield.ac.uk)'}))
    
    forename = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Forename'}))
    
    surname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    
    department = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'University department'}))
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    
    class Meta:
        model = CustomUser
        fields = ('email', 'forename', 'surname', 'department', 'password1', 'password2')


class StudentCreationForm(forms.ModelForm):

    course = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'University course'}))
    
    support_plan = forms.FileField(label='Upload your learning support plan (if applicable)',
        widget=forms.FileInput(attrs={'placeholder': 'Support plan'}))

    class Meta:
        model = Student
        fields = ('course', 'support_plan')