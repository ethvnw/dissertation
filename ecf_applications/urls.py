from django.urls import path

from . import views

app_name = "ecf_application"

urlpatterns = [
    path("new/", views.NewECFApplicationWizardView.as_view(), name="new"),
    path("success/", views.ECFApplicationSuccessView.as_view(), name="success"),
    path("detail/<int:pk>/", views.ECFApplicationDetailView.as_view(), name="detail"),
    path("comment/<int:pk>/", views.CommentSendView.as_view(), name="comment"),
    path("edit/<int:pk>/", views.ECFApplicationEditView.as_view(), name="edit"),
]