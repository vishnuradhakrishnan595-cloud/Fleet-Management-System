from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('fleet_manager', 'Fleet Manager'),
        ('dispatcher', 'Dispatcher'),
        ('driver', 'Driver'),
        ('accountant', 'Accountant'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='driver'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
