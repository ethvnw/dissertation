from django import forms

from authentication.models import Student, User


class StudentProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'
            visible.field.widget.attrs['placeholder'] = visible.label

    template_name = "dashboard/form.html"

    study_level = forms.ChoiceField(
        choices=[("", "Select Your Level of Study")] + Student.STUDY_LEVELS,
        widget=forms.Select
    )

    course = forms.CharField(
        label="Course programme",
        max_length=250,
        widget=forms.TextInput
    )

    support_plan = forms.FileField(
        label="Upload a support plan (overrides any existing)",
        required=False,
        widget=forms.FileInput
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "department", "study_level", "course", "support_plan"]


class StaffProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffProfileForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'
            visible.field.widget.attrs['placeholder'] = visible.label

    template_name = "dashboard/form.html"

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "department"]