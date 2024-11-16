from django.contrib import admin
from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
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


admin.site.register(CustomUser, UserAdmin)
