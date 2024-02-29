from django.urls import path
from . import views

app_name = 'ecfapps'
urlpatterns = [
    path('new/', views.ECFAppWizard.as_view(), name='new'),
    path('success/', views.success, name='success'),
]
