from django.db import models

# Create your models here.

from django.db import models
from vehicles.models import Vehicle
from django.conf import settings


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('fuel', 'Fuel'),
        ('maintenance', 'Maintenance'),
        ('insurance', 'Insurance'),
        ('salary', 'Driver Salary'),
        ('toll', 'Toll'),
        ('parking', 'Parking'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    title = models.CharField(max_length=255)

    amount = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    expense_date = models.DateField()

    description = models.TextField(blank=True)

    receipt = models.FileField(
        upload_to='expense_receipts/',
        null=True,
        blank=True
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
