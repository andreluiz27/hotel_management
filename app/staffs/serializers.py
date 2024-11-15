from rest_framework import serializers
from .models import Staff  # todo: change this to User
from core.tasks import send_email_task
from core.settings import EMAIL_HOST_USER


class UserSerializer(
    serializers.ModelSerializer
):  # todo: change this to  UserSerializer

    class Meta:
        model = Staff  # Todo: change this to User
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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff  # todo: change this to User
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "state",
            "zip_code",
        ]

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        send_email_task.delay(
            "Welcome to the Hotel Reservation System",
            message="Welcome",
            receiver=instance.email,
            sender=EMAIL_HOST_USER,
        )

        return instance


class UserStaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff  # todo: change this to User
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "state",
            "zip_code",
        ]


class UserGuestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff  # todo: change this to User
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "state",
            "zip_code",
        ]

        def save(self, **kwargs):
            instance = super().save(**kwargs)
            send_email_task.delay(
                "Welcome to the Hotel Reservation System",
                message="Welcome",
                receiver=instance.email,
                sender=EMAIL_HOST_USER,
            )

            return instance
