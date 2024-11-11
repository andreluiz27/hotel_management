from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Staff(AbstractUser):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
