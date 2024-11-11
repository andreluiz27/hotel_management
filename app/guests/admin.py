from django.contrib import admin
from guests.models import Guest


class GuestAdmin(admin.ModelAdmin):
    # displaying all the fields in the admin panel
    list_display = ("id", "name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)

    class Meta:
        model = Guest


admin.site.register(Guest, GuestAdmin)
admin.sites.AdminSite.site_header = "Anima Test ADMIN"
