
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Vehicle(models.Model):

    VEHICLE_TYPES = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('bus', 'Bus'),
        ('car', 'Car'),
        ('pickup', 'Pickup'),
        ('trailer', 'Trailer'),
        ('other', 'Other'),
    ]

    FUEL_TYPES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('cng', 'CNG'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('inactive', 'Inactive'),
    ]

    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )

    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Capacity in kilograms"
    )

    registration_date = models.DateField()
    insurance_expiry = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    image = models.ImageField(
        upload_to='vehicle_images/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_name}"

    class Meta:
        ordering = ['-created_at']
