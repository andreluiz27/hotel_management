from rest_framework import serializers
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "state",
            "zip_code",
        ]


