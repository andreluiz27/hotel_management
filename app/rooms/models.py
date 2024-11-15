from django.db import models

# Create your models here.


class Room(models.Model):

    room_status_choices = [
        ("Available", "Available"),
        ("Occupied", "Occupied"),
        ("Maintenance", "Maintenance"),
        ("Cleaning", "Cleaning"),
        ("Out of Service", "Out of Service"),
    ]

    room_type_choices = [
        ("Single", "Single"),
        ("Double", "Double"),
        ("Luxury Single", "Luxury Single"),
        ("Luxury Double", "Luxury Double"),
    ]

    id = models.IntegerField(primary_key=True)
    room_status = models.CharField(choices=room_status_choices)
    floor = models.IntegerField()
    room_type = models.CharField(max_length=255, choices=room_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   

    def __str__(self):
        return str(self.id)
