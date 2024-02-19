from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Student

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.label = ""

    template_name = "accounts/form.html"

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Email (@sheffield.ac.uk)'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Password'}))


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.label = ""

    template_name = "accounts/form.html"

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@sheffield.ac.uk" not in data:
            raise forms.ValidationError("Must be a valid sheffield.ac.uk address")
        
        return data

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Email (@sheffield.ac.uk)'}))
    
    forename = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'First name'}))
    
    surname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Last name'}))
    
    department = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'University department'}))
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Password'}),
        )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'Confirm password'}))

    
    class Meta:
        model = CustomUser
        fields = ('email', 'forename', 'surname', 'department', 'password1', 'password2')


class StudentCreationForm(forms.ModelForm):
    template_name = "accounts/form.html"

    course = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'bg-transparent rounded-sm border-uni-violet mb-2 w-full',
            'placeholder': 'University course'}))
    
    support_plan = forms.FileField(
        required=False,
        label='Upload your learning support plan (if applicable)',
        widget=forms.FileInput(attrs={
            'class': 'mt-2',
            'placeholder': 'Support plan'}))

    class Meta:
        model = Student
        fields = ('course', 'support_plan')