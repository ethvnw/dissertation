from django.contrib import admin

from ecf_applications.models import ECFApplication, ECFApplicationAssessment, ECFApplicationComment, ECFApplicationAssessmentComment

# Register your models here.
admin.site.register(ECFApplication)
admin.site.register(ECFApplicationAssessment)
admin.site.register(ECFApplicationComment)
admin.site.register(ECFApplicationAssessmentComment)