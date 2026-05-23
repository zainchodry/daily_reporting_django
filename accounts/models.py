from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"

    class Meta:
        ordering = ['username']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    joined_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Profile of {self.user.username}"