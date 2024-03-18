from django.utils import timezone
from django import forms

from .models import Meeting


class MeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'

   
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "bg-transparent rounded-sm border-uni-violet mb-2 w-full",
            }
        ),
    )

    def clean_date_time(self):
        date_time = self.cleaned_data['date_time']
        if date_time < timezone.now():
            raise forms.ValidationError("The date cannot be in the past")
        return date_time
    
    class Meta:
        model = Meeting
        fields = ("category", "date_time")
