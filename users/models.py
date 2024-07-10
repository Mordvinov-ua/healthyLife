from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to = "users_images", blank = True, null = True)
    phone_code = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    street_and_house_number = models.CharField(max_length=255, blank=True, null=True)
    additional_address = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ("id",)

    
