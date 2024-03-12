from django.urls import path

from . import views

urlpatterns = [
    path ("", views.index, name="index"),
    path("download/", views.DownloadView.as_view(), name="download"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
