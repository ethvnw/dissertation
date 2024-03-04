import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    department = models.CharField(
        max_length=5,
        choices=settings.DEPARTMENTS,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['forename', 'surname', 'department']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.forename} {self.surname}"
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    course = models.CharField(max_length=50)
    support_plan = models.FileField(upload_to='support_plans/', null=True, blank=True)

    def support_plan_file(self):
        return os.path.basename(self.support_plan.name)

    def __str__(self):
        return f"{self.user.forename} {self.user.surname}"
