from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from vehicles.models import Vehicle


class Incident(models.Model):

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='incidents'
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    title = models.CharField(max_length=255)

    incident_type = models.CharField(max_length=100)

    description = models.TextField()

    location = models.CharField(max_length=255)

    incident_date = models.DateTimeField()

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='low'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='reported'
    )

    estimated_damage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    evidence = models.FileField(
        upload_to='incident_evidence/',
        null=True,
        blank=True
    )

    resolution_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
