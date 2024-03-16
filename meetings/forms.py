from django import forms

from .models import Meeting


class MeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-transparent rounded-sm border-uni-violet mb-2 w-full'

   
    # date_time with timezone support
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "bg-transparent rounded-sm border-uni-violet mb-2 w-full",
            }
        ),
    )

    class Meta:
        model = Meeting
        fields = ("category", "date_time")
