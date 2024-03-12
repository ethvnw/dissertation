from django import forms

from authentication.models import Student, User


class ProfileForm(forms.ModelForm):
    template_name = "dashboard/form.html"

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if visible.field.widget.__class__.__name__ == "RadioSelect":
                visible.field.widget.attrs['class'] = 'mb-2'
            else:
                visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "department"]


class StudentProfileForm(forms.ModelForm):
    template_name = "dashboard/form.html"

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if visible.field.widget.__class__.__name__ == "RadioSelect":
                visible.field.widget.attrs['class'] = 'mb-2'
            else:
                visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'


    support_plan = forms.FileField(
        label="Upload a new support plan (overrides any existing)",
        required=False,
        widget=forms.FileInput
    )


    class Meta:
        model = Student 
        fields = ["study_level", "course", "support_plan"]