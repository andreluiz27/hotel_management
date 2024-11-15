from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

# Create your models here.


class Staff(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name

    class Meta:
        permissions = [
            ("can_do_checkin", "Can do checkin"),
            ("can_do_checkout", "Can do checkout"),
        ]
