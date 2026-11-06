from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from vehicles.models import Vehicle


class Trip(models.Model):

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='trips'
    )

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_trips'
    )

    start_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    starting_odometer = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    ending_odometer = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )

    distance = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0
    )

    purpose = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.destination}"

    def save(self, *args, **kwargs):
        if self.ending_odometer is not None:
            self.distance = max(
                0,
                self.ending_odometer - self.starting_odometer
            )
        super().save(*args, **kwargs)
