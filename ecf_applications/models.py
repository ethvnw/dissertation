import os

from django.db import models
from django.urls import reverse

CODES = {
    "PENDING": 1, # first submitted / not assigned to meeting
    "ACTION_REQUIRED": 2, # student needs to edit details
    "UNDER_REVIEW": 3, # assigned to scrutiny meeting
    "UNDER_EXAM_REVIEW": 4, # assigned to exam board meeting
    "REJECTED": 5,
    "APPROVED": 6,
    "PARTIAL_APPROVAL": 7,
}

STATUS_CHOICES = [
    (CODES["PENDING"], "Pending"),
    (CODES["ACTION_REQUIRED"], "Action Required"),
    (CODES["UNDER_REVIEW"], "Under Review"),
    (CODES["UNDER_EXAM_REVIEW"], "Under Exam Board Review"),
    (CODES["REJECTED"], "Rejected"),
    (CODES["APPROVED"], "Approved"),
    (CODES["PARTIAL_APPROVAL"], "Partially Approved"),
]

class ECFApplication(models.Model):
    applicant = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    submission_date = models.DateTimeField("submission date", auto_now_add=True)

    status = models.PositiveSmallIntegerField("status", choices=STATUS_CHOICES, default=1)

    start_date = models.DateField("start date")
    end_date = models.DateField("end date", null=True, blank=True)

    CIRCUMSTANCE_CHOICES = [
        (1, 'Adverse Personal or Family Circumstances'),
        (2, 'Bereavement'),
        (3, 'Long Term Medical Condition'),
        (4, 'Short Term Medical Episode'),
        (5, 'Other'),
    ]
    circumstance = models.PositiveSmallIntegerField("circumstance", choices=CIRCUMSTANCE_CHOICES)

    description = models.TextField("description")

    def gen_file_name(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s_evidence.%s" % (instance.id, ext)
        return os.path.join('evidence', filename)
    
    evidence = models.FileField("evidence", upload_to=gen_file_name, null=True, blank=True)

    last_modified = models.DateTimeField("last modified", auto_now=True)

    def get_absolute_url(self):
        return reverse("ecf_application:detail", kwargs={"pk": self.pk})

    
class ECFApplicationAssessment(models.Model):
    application = models.ForeignKey("ecf_applications.ECFApplication", on_delete=models.CASCADE)

    status = models.PositiveSmallIntegerField("status", choices=STATUS_CHOICES, default=1)
    module = models.CharField("module code", max_length=15)
    assessment = models.CharField("assessment name", max_length=200)

    AUTHORISED_ABSENCE = 1
    EXAM_BOARD_CONSIDERATION = 2
    EXTENSION = 3
    LATE_PENALTY_REMOVAL = 4
    NOT_ASSESSED = 5
    OTHER = 6

    ACTION_CHOICES = [
        (AUTHORISED_ABSENCE, "Authorised Absence"),
        (EXAM_BOARD_CONSIDERATION, "Exam Board Consideration"),
        (EXTENSION, "Extension"),
        (LATE_PENALTY_REMOVAL, "Late Penalty Removal"),
        (NOT_ASSESSED, "Not Assessed"),
        (OTHER, "Other"),
    ]
    action = models.PositiveSmallIntegerField("action", choices=ACTION_CHOICES)

    extension_date = models.DateField("extension date", null=True, blank=True)
    description = models.TextField("description")


class ECFApplicationComment(models.Model):
    application = models.ForeignKey("ecf_applications.ECFApplication", on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    comment = models.TextField("comment")
    date = models.DateTimeField("date", auto_now_add=True)


class ECFApplicationAssessmentComment(models.Model):
    assessment = models.ForeignKey("ecf_applications.ECFApplicationAssessment", on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    comment = models.TextField("comment")
    date = models.DateTimeField("date", auto_now_add=True) 
