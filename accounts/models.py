from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    department = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['forename', 'surname', 'department']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.forename} {self.surname}"
    

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
    course = models.CharField(max_length=50)
    support_plan = models.FileField(upload_to='support_plans/', null=True, blank=True)
