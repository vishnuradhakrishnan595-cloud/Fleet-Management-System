from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'first_name',
        'last_name',
        'phone',
        'license_number',
        'license_expiry',
        'status',
    )

    list_filter = (
        'status',
        'license_type',
    )

    search_fields = (
        'employee_id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'license_number',
    )

    ordering = ('-created_at',)
    list_per_page = 20