from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Fleet Management Information', {
            'fields': (
                'role',
                'phone',
                'address',
                'profile_picture',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Fleet Management Information', {
            'fields': (
                'role',
                'phone',
                'address',
                'profile_picture',
            )
        }),
    )
