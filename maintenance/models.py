from django.db import models

# Create your models here.

from django.db import models
from vehicles.models import Vehicle
from django.conf import settings


class Maintenance(models.Model):

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    MAINTENANCE_TYPES = [
        ('service', 'Regular Service'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('tyre', 'Tyre Replacement'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )

    maintenance_type = models.CharField(
        max_length=30,
        choices=MAINTENANCE_TYPES
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    service_date = models.DateField()

    next_service_date = models.DateField(
        null=True, blank=True
    )

    odometer_reading = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    service_center = models.CharField(max_length=255)

    cost = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
