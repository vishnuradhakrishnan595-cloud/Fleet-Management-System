from django.db import models

# Create your models here.

from django.db import models
from vehicles.models import Vehicle
from django.conf import settings


class Document(models.Model):

    DOCUMENT_TYPES = [
        ('registration', 'Registration Certificate'),
        ('insurance', 'Insurance'),
        ('permit', 'Permit'),
        ('license', 'Driving License'),
        ('pollution', 'Pollution Certificate'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    title = models.CharField(max_length=255)

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES
    )

    file = models.FileField(
        upload_to='vehicle_documents/'
    )

    issue_date = models.DateField(
        null=True, blank=True
    )

    expiry_date = models.DateField(
        null=True, blank=True
    )

    description = models.TextField(blank=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
