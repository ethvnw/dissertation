from django.contrib import admin

from ecfapps.models import ECFApplication, ECFApplicationModuleAssessment

# Register your models here.
admin.site.register(ECFApplication)
admin.site.register(ECFApplicationModuleAssessment)