from rest_framework import serializers
from .models import Reservation
from rooms.serializers import RoomSerializer
from guests.serializers import GuestSerializer
from core.tasks import send_email_task
from core.settings import EMAIL_HOST_USER, MAILING_ACTIVE


class ReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    guest = GuestSerializer()
    staff = serializers.SerializerMethodField("get_staff")

    def get_staff(self, obj):
        return {
            "first_name": obj.staff.first_name,
            "last_name": obj.staff.last_name,
            "email": obj.staff.email,
            "id": obj.staff.id,
        }

    class Meta:
        model = Reservation
        fields = [
            "id",
            "room",
            "reservation_status",
            "guest",
            "staff",
            "payment_status",
            "payment_method",
            "paid_amount",
        ]


class CreateReservationSerializer(serializers.ModelSerializer):
    # not asking the id of the reservation, because it is autoincremented
    # creating a pk field with autoincremented
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "date_start",
            "date_end",
            "reservation_status",
            "payment_status",
            "paid_amount",
            "payment_method",
            "guest",
            "staff",
            "room",
        ]
        extra_kwargs = {
            "date_start": {"required": True},
            "date_end": {"required": True},
            "reservation_status": {"required": True},
            "payment_status": {"required": True},
            "guest": {"required": True},
            "staff": {"required": True},
        }

    def validate(self, data):
        if data["date_start"] > data["date_end"]:
            raise serializers.ValidationError(
                "The start date must be before the end date."
            )

        if data.get("room", None) and data["room"].room_status != "Available":
            raise serializers.ValidationError("The room is not available.")

        if data["reservation_status"] not in ["Confirmed", "On Hold"]:
            raise serializers.ValidationError(
                "Reservation status must be Confirmed or On Hold"
            )

        return data

    def save(self):
        instance = super().save()

        if instance.room:
            instance.room.room_status = "Occupied"
            instance.room.save()

        if MAILING_ACTIVE:
            send_email_task.delay(
                subject="Reservation Created",
                message="Your reservation has been created.",
                data={
                    "reservation_id": instance.id,
                    "guest": instance.staff.email,  # todo: change staff to user
                },
                sender=EMAIL_HOST_USER,
                receiver=instance.staff.email,
            )

        return instance


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "reservation_status",
            "room",
            "payment_status",
            "payment_method",
            "paid_amount",
        ]

    def save(self):
        instance = super().save()

        send_email_task.delay(
            "Reservation Updated",
            {
                "reservation_id": instance.id,
                "guest": instance.staff.email,  # todo: change staff to user
            },
            "Your reservation has been updated.",
        )

        return instance


class ReservationUpdateCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["room", "payment_method", "paid_amount"]
        extra_kwargs = {
            "room": {"required": False},
            "payment_method": {"required": False},
            "paid_amount": {"required": False},
        }

    def validate(self, data):
        # check if this reservation is already checked in
        if self.instance.reservation_status == "Checked In":
            raise serializers.ValidationError(
                "Reservation is already checked in."
            )

        # if the reservation does not have a room, the room field is required
        if not self.instance.room and not data.get("room", None):
            raise serializers.ValidationError("Room is required.")

        # check if the room is available
        if data.get("room", None) and data["room"].room_status != "Available":
            raise serializers.ValidationError("The room is not available.")

        # check if checkin paid amount is positive
        if data.get("paid_amount", None) and data["paid_amount"] < 0:
            raise serializers.ValidationError("Paid amount must be positive.")

        # if reservation is already paid, the payment fields are not required
        if self.instance.payment_status == "Paid" and (
            data.get("payment_method", None) or data.get("paid_amount", None)
        ):
            raise serializers.ValidationError(
                "Payment fields are not required,reservation is already paid."
            )

        if self.instance.payment_status != "Paid" and (
            not data.get("payment_method", None)
            or not data.get("paid_amount", None)
        ):
            raise serializers.ValidationError(
                "Payment fields are required, reservation is not paid."
            )

        return data

    def save(self):
        instance = super().save()

        if instance.room:
            instance.room.room_status = "Occupied"
            instance.room.save()

        instance.reservation_status = "Checked In"
        instance.payment_status = "Paid"
        instance.save()
        if MAILING_ACTIVE:
            send_email_task.delay(
                "Reservation Checked In",
                {
                    "reservation_id": instance.id,
                    "guest": instance.staff.email,  # todo: change staff to user
                },
                "Your reservation has been checked in.",
            )

        return instance


class ReservationUpdateCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = []

    def validate(self, data):
        # check if this reservation is already checked out
        if self.instance.reservation_status == "Checked Out":
            raise serializers.ValidationError(
                "Reservation is already checked out."
            )
        if self.instance.reservation_status != "Checked In":
            raise serializers.ValidationError(
                "Reservation is not checked in."
            )

        return data

    def save(self):
        instance = super().save()

        instance.reservation_status = "Checked Out"
        instance.room.room_status = "Cleaning"
        instance.save()
        send_email_task.delay(
            subject="Reservation Checked Out",
            data={
                "reservation_id": instance.id,
                "guest": instance.staff.email,  # todo: change staff to user
            },
            message="Your reservation has been checked out.",
            sender=EMAIL_HOST_USER,
            receiver=instance.staff.email,
        )

        return instance


# class RSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"


# class RoomUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = ["room_status"]
