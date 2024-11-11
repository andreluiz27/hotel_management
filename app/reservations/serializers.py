from rest_framework import serializers
from .models import Reservation
from rooms.serializers import RoomSerializer
from guests.serializers import GuestSerializer


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


class ReservationUpdateCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["room", "payment_method", "paid_amount"]
        extra_kwargs = {
            "room": {"required": False},
            "payment_method": {"required": True},
            "paid_amount": {"required": True},
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

        return data

    def save(self):
        instance = super().save()

        if instance.room:
            instance.room.room_status = "Occupied"
            instance.room.save()

        instance.reservation_status = "Checked In"
        instance.payment_status = "Paid"
        instance.save()
        return instance


# class RSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"


# class RoomUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = ["room_status"]
