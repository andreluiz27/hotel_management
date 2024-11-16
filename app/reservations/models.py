from django.db import models

# Create your models here.


class Reservation(models.Model):

    payment_status_choices = [
        ("Paid", "Paid"),
        ("Pendent", "Pendent"),
    ]

    reservation_status_choices = [
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("On Hold", "On Hold"),
        ("Checked In", "Checked In"),
        ("Checked Out", "Checked Out"),
    ]

    paymentmethod_status_choices = [
        ("Cash", "Cash"),
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
        ("Pix", "Pix"),
    ]

    id = models.AutoField(primary_key=True)

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)

    reservation_status = models.CharField(
        max_length=255,
        choices=reservation_status_choices,
        blank=True,
        null=True,
    )
    payment_status = models.CharField(
        max_length=255, choices=payment_status_choices, default="Pendent"
    )
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    payment_method = models.CharField(
        max_length=255,
        choices=paymentmethod_status_choices,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # foreign keys
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return str(self.id)
