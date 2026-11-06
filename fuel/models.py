from django.db import models

# Create your models here.

from django.db import models
from vehicles.models import Vehicle
from django.conf import settings


class FuelRecord(models.Model):

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
        ('electric', 'Electric'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='fuel_records'
    )

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES
    )

    quantity = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    price_per_unit = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    total_cost = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    odometer_reading = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    fuel_date = models.DateField()

    station_name = models.CharField(
        max_length=255, blank=True
    )

    receipt = models.FileField(
        upload_to='fuel_receipts/',
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.fuel_date}"
