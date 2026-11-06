from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        'vehicle_number',
        'vehicle_name',
        'vehicle_type',
        'brand',
        'fuel_type',
        'capacity',
        'status',
    )

    list_filter = ('vehicle_type', 'fuel_type', 'status')

    search_fields = (
        'vehicle_number',
        'vehicle_name',
        'brand',
        'model',
    )

    list_per_page = 20
