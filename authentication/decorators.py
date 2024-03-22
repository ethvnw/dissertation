from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == 1,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    return actual_decorator(function)


def secretary_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == 2,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(function)


def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.role == 2 or u.role == 3),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(function)
