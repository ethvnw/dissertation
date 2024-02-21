from django.db import models

# Create your models here.
class ECFApplication(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('PE', 'Pending'),
        ('AR', 'Action Required'),
        ('AP', 'Approved'),
        ('RE', 'Rejected')
    ]
    status = models.fields.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='PE',
    )

    CIRCUMSTANCE_CHOICES = [
        ('SM', 'Short Term Medical Episode'),
        ('LM', 'Long Term Medical Condition'),
        ('BE', 'Bereavement'),
        ('PE', 'Adverse Personal or Family Circumstances'),
        ('OT', 'Other'),
    ]
    circumstance = models.CharField(
        max_length=2,
        choices=CIRCUMSTANCE_CHOICES,
    )

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()                                
    evidence = models.FileField(upload_to='evidence/', null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.get_circumstance_display()} ({self.submission_date})"


class ECFApplicationModuleAssessment(models.Model):
    application = models.ForeignKey(ECFApplication, on_delete=models.CASCADE)
    module_code = models.CharField(max_length=10)
    assessment = models.CharField(max_length=100)

    ACTION_CHOICES = [
        ('EX', 'Extension'),
        ('NA', 'Not Assessed'),
        ('LR', 'Late Penalty Removal'),
        ('BC', 'Exam Board Consideration'),
        ('AA', 'Authorised Absence'),
        ('OT', 'Other'),
    ]
    action = models.CharField(
        max_length=2,
        choices=ACTION_CHOICES,
    )

    extension_date = models.DateField(null=True, blank=True)
    more_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.application} - {self.module_code}"
