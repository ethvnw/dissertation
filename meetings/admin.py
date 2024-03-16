from django.contrib import admin

from meetings.models import Meeting, MeetingAgenda

# Register your models here.
admin.site.register(Meeting)
admin.site.register(MeetingAgenda)