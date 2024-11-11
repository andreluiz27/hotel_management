from django.contrib import admin
from reservations.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guest",
        "staff",
        "room",
        "payment_method",
        "paid_amount",
        "payment_status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "check_in",
        "check_out",
    )
    list_filter = ("created_at", "updated_at")

    class Meta:
        model = Reservation


admin.site.register(Reservation, ReservationAdmin)
