from django.db import models

class Notification(models.Model):
    application = models.ForeignKey("ecf_applications.ECFApplication", on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
