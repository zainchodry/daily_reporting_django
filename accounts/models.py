from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    Role_Choices = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=Role_Choices, default='employee')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=12,
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
        return self.user.username
    