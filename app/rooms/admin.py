from django.contrib import admin
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "room_status",
        "floor",
        "room_type",
        "created_at",
        "updated_at",
    ]
    search_fields = ["floor", "room_type"]
    list_filter = ["floor", "room_type"]

    class Meta:
        model = Room


admin.site.register(Room, RoomAdmin)
