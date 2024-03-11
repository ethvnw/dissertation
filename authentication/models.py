import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from .managers import NewUserManager


class User(AbstractUser):
    email = models.EmailField("email", unique=True)
    username = None
    department = models.CharField("department",
        max_length=5,
        choices=settings.DEPARTMENTS
    )

    STUDENT = 1
    SECRETARY = 2
    SCRUTINY = 3
    role = models.PositiveSmallIntegerField("role",
        choices=[
            (STUDENT, "student"),
            (SECRETARY, "secretary"),
            (SCRUTINY, "scrutiny"),
        ],
        default=1
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "department"]

    objects = NewUserManager()

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    STUDY_LEVELS = [
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
        (5, 'Postgraduate'),
    ]

    def gen_file_name(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s_support_plan.%s" % (instance.user.id, ext)
        return os.path.join('support_plans', filename)
    
    study_level = models.PositiveSmallIntegerField("study level", choices=STUDY_LEVELS)
    course = models.CharField("course", max_length=250)
    support_plan = models.FileField(upload_to=gen_file_name, null=True, blank=True)



