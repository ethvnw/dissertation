from django.urls import path

from . import views

app_name = "meetings"

urlpatterns = [
    path("new/", views.MeetingCreateView.as_view(), name="new"),
    path("detail/<int:pk>/", views.MeetingDetailView.as_view(), name="detail"),
    path("list/", views.MeetingListView.as_view(), name="list"),
]