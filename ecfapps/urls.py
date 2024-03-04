from django.urls import path
from . import views

app_name = 'ecfapps'
urlpatterns = [
    path('new/', views.ECFAppWizard.as_view(), name='new'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('success/', views.success, name='success'),
]
