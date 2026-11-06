from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import RegexValidator


class Driver(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('on_leave', 'On Leave'),
        ('inactive', 'Inactive'),
    ]

    LICENSE_TYPE_CHOICES = [
        ('LMV', 'Light Motor Vehicle'),
        ('HMV', 'Heavy Motor Vehicle'),
        ('HGMV', 'Heavy Goods Motor Vehicle'),
        ('HPMV', 'Heavy Passenger Motor Vehicle'),
        ('MCWG', 'Motorcycle With Gear'),
        ('OTHER', 'Other'),
    ]

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^[0-9+\-\s()]{7,15}$',
                message='Enter a valid phone number.'
            )
        ]
    )

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    license_type = models.CharField(
        max_length=10,
        choices=LICENSE_TYPE_CHOICES
    )

    license_expiry = models.DateField()

    date_of_joining = models.DateField()

    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"