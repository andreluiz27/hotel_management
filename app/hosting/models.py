from django.db import models

# Create your models here.


class Hosting(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # foreign keys
    guest_id = models.ForeignKey("guests.Guest", on_delete=models.CASCADE)
    reservation_id = models.ForeignKey(
        "reservations.Reservation", on_delete=models.CASCADE
    )
    room_id = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
