from django.db import models
from django.urls import reverse


class Meeting(models.Model):
    SCRUTINY_PANEL = 1
    EXAM_BOARD = 2

    CATEGORY_CHOICES = [
        (SCRUTINY_PANEL, "Scrutiny Panel"),
        (EXAM_BOARD, "Exam Board"),
    ]
    creator = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    category = models.SmallIntegerField("type of meeting", choices=CATEGORY_CHOICES)
    date_time =  models.DateTimeField("date and time of meeting", auto_now=False, auto_now_add=False)
    
    def get_absolute_url(self):
        return reverse("meetings:detail", kwargs={"pk": self.pk})
    
    
class MeetingAgenda(models.Model):
    application = models.ForeignKey("ecf_applications.ECFApplication", on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
