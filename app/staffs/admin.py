from django.contrib import admin
from staffs.models import Staff


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "role",
        "email",
        "phone",
        "address",
        "city",
        "state",
        "country",
        "zip_code",
        "updated_at",
    )


admin.site.register(Staff, StaffAdmin)
