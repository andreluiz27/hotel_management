from reservations.models import Reservation
from django.urls import reverse
from staffs.models import Staff
from rooms.models import Room
from django.contrib.auth.models import Group
import json
from random import randint

DEFAULT_PASSWORD = "passfortest"


def make_reservation_in_db(
    date_start,
    date_end,
    reservation_status,
    payment_status,
    paid_amount,
    payment_method,
    guest_id,
    staff_id,
    room_id,
):
    reservation = Reservation(
        date_start=date_start,
        date_end=date_end,
        reservation_status=reservation_status,
        payment_status=payment_status,
        paid_amount=paid_amount if paid_amount else 0,
        payment_method=payment_method if payment_method else None,
        guest_id=guest_id,
        staff_id=staff_id,
        room_id=room_id,
    )
    reservation.save()
    return reservation


def make_user_in_db(email, password, role, username):
    user = Staff.objects.create_user(
        username=username, email=email, password=password
    )  # todo: change Staff to User
    user.role = role
    user.save()
    return user


def make_random_email():
    return "random_user_email" + str(randint(0, 999999)) + "@example.com"


def make_random_username():
    return "random_user" + str(randint(0, 999999))


def make_guest_in_db():
    random_number = str(
        randint(0, 999999)
    )  # to avoid unique constraint in emails
    guest = make_user_in_db(
        email=make_random_email(),
        password=DEFAULT_PASSWORD,
        role=get_role_in_db("Guest"),
        username="guest" + random_number,
    )
    return guest


def get_room_in_db_by_status(room_status):
    room = Room.objects.all().first()
    room.room_status = room_status
    room.save()
    return room


def make_checkin_url(reservation_id):
    return reverse("reservation-update-checkin", args=[reservation_id])


def make_checkout_url(reservation_id):
    return reverse("reservation-update-checkout", args=[reservation_id])


def make_room_detail_url(room_id):
    return reverse("room-detail", args=[room_id])


def make_checkin_payload(room_id, payment_method, paid_amount):
    return {
        "room": room_id,
        "payment_method": payment_method,
        "paid_amount": paid_amount,
    }


def make_reservation_payload(
    date_start,
    date_end,
    reservation_status,
    payment_status,
    paid_amount,
    payment_method,
    guest,
    staff,
    room,
):
    return {
        "date_start": date_start,
        "date_end": date_end,
        "reservation_status": reservation_status,
        "payment_status": payment_status,
        "paid_amount": paid_amount,
        "payment_method": payment_method,
        "guest": guest,
        "staff": staff,
        "room": room,
    }


def get_token(email, password, request_client):
    credentials = {"username": email, "password": password}
    response = request_client.post(
        reverse("token_obtain_pair"),
        credentials,
        format="json",
    )
    return response.data["access"]


def get_manager_staff_token(request_client):
    email = make_random_email()
    manager_staff = make_user_in_db(
        username=make_random_username(),
        email=make_random_email(),
        password=DEFAULT_PASSWORD,
        role=get_role_in_db("ManagerStaff"),
    )
    email = manager_staff.email  # todo refactor that
    response_token = get_token(
        email=email,
        password=DEFAULT_PASSWORD,
        request_client=request_client,
    )
    return response_token


def get_regular_staff_token(request_client):
    email = make_random_email()
    regular_staff = make_user_in_db(
        username=make_random_username(),
        email=email,
        password=DEFAULT_PASSWORD,
        role=get_role_in_db("RegularStaff"),
    )
    email = regular_staff.email
    response_token = get_token(
        email=email,
        password=DEFAULT_PASSWORD,
        request_client=request_client,
    )
    return response_token


def get_guest_token(request_client):
    email = make_random_email()
    guest = make_user_in_db(
        username=make_random_username(),
        email=email,
        password=DEFAULT_PASSWORD,
        role=get_role_in_db("Guest"),
    )
    email = guest.email
    response_token = get_token(
        email=email,
        password=DEFAULT_PASSWORD,
        request_client=request_client,
    )
    return response_token


def get_role_in_db(role):
    return Group.objects.get(name=role)
