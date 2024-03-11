from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        'signin/',
        views.StudentSignInView.as_view(),
        name='signin'
    ),
    path(
        'signout/',
        views.signout,
        name='signout'
    ),

    path('signup/', views.StudentSignUpView.as_view(), name='signup')
]
