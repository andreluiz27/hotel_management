from rest_framework import serializers
from .models import Guest


class GuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guest
        fields = [
            "id",
            "name",
            "email",
            "address",
            "city",
            "state",
            "zip_code",
        ]
