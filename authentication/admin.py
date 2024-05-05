from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import StudentSignUpForm
from .models import User, Student

class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'department', 'role', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'department', 'role')

    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'department', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'department', 'role'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Student)