from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction

from .models import Student, User


class StudentSignUpForm(UserCreationForm):
    
    template_name = 'authentication/form.html'

    department_choices = {"": "Select Your Department"}
    department_choices.update(settings.DEPARTMENTS)

    department = forms.ChoiceField(
        choices=department_choices,
        widget=forms.Select
    )

    study_level = forms.ChoiceField(
        choices=[("", "Select Your Level of Study")] + Student.STUDY_LEVELS,
        widget=forms.Select
    )

    course = forms.CharField(
        label="Course Programme",
        max_length=250,
        widget=forms.TextInput
    )

    support_plan = forms.FileField(
        label="Support Plan (optional)",
        required=False,
        widget=forms.FileInput
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'first_name', 'last_name', 'department']

    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'
            visible.field.widget.attrs['placeholder'] = visible.label
            
            if not visible.field.widget.__class__.__name__ == 'FileInput':
                visible.label = ""

    @transaction.atomic
    def save(self):
        user = super().save()

        student = Student(user=user)
        student.study_level = self.cleaned_data.get('study_level')
        student.course = self.cleaned_data.get('course')
        student.support_plan = self.cleaned_data.get('support_plan')
        student.save()

        return user


class StudentSignInForm(AuthenticationForm):
    template_name = 'authentication/form.html'

    def __init__(self, *args, **kwargs):
        super(StudentSignInForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'
            visible.field.widget.attrs['placeholder'] = visible.label
            visible.label = ""
