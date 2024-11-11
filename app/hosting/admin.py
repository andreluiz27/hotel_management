from django.contrib import admin
from hosting.models import Hosting


class HostingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone",
        "address",
        "city",
        "state",
        "country",
        "zip_code",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "email",
        "phone",
        "address",
        "city",
        "state",
        "country",
        "zip_code",
    )
    list_filter = ("created_at", "updated_at")

    class Meta:
        model = Hosting


admin.site.register(Hosting, HostingAdmin)
