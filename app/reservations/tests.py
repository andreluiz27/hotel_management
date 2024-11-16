from django.test import TestCase
from django.urls import reverse
from .models import Reservation
from helpers_tests import (
    make_reservation_in_db,
    make_user_in_db,
    make_checkin_url,
    make_checkin_payload,
    make_reservation_payload,
    make_guest_in_db,
    make_checkout_url,
    get_token,
    get_role_in_db,
    get_regular_staff_token,
    get_room_in_db_by_status,
    DEFAULT_PASSWORD,
)
from core.settings import TEST_LOGGER_LEVEL
import json
import logging


logging.basicConfig(
    level=TEST_LOGGER_LEVEL, format="%(message)s - %(asctime)s"
)
TestLogger = logging.getLogger(__name__)


# CONSTANTS
AVAILABLE_ROOM_ID = 103
NOT_AVAILABLE_ROOM_ID = 101
POSSIBLE_STATUS_AFTER_CREATION = ["Confirmed", "On Hold"]
RESERVATION_ID = 5
AVAILABLE_ROOM_ID = 300


# PAYLOADS
NEW_RESERVATION_PAYLOAD = {
    "date_start": "2022-01-01T00:00:00Z",
    "date_end": "2022-01-02T00:00:00Z",
    "reservation_status": "Confirmed",
    "payment_status": "Paid",
    "paid_amount": 100.0,
    "payment_method": "Credit Card",
    "user": 2,
    "room": AVAILABLE_ROOM_ID,
}

# URLS
CREATE_RESERVATION_URL = reverse("reservation-create")
CHECKIN_RESERVATION_URL = reverse(
    "reservation-update-checkin", args=[RESERVATION_ID]
)

# TEST CASES


class ReservationTestCase(TestCase):
    fixtures = ["initial_test_data.json"]

    def test_reservation_creation_endpoint(self):
        regular_staff_token = get_regular_staff_token(self.client)
        room_available = get_room_in_db_by_status("Available")
        owner_of_reservation = make_guest_in_db()

        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user=owner_of_reservation.id,
            room=room_available.id,
        )
        response = self.client.post(
            CREATE_RESERVATION_URL,
            json.dumps(new_reservation_payload),
            headers={"Authorization": f"Bearer {regular_staff_token}"},
            content_type="application/json",
        )

        try:
            self.assertEqual(response.status_code, 201)
        except AssertionError:
            TestLogger.debug(response.data)
            raise AssertionError

        # check if the reservation was created
        just_created_reservation = response.data["id"]
        reservation_in_db = Reservation.objects.get(
            pk=just_created_reservation
        )
        self.assertEqual(just_created_reservation, reservation_in_db.id)

        # check if the room is not available anymore
        room = reservation_in_db.room
        self.assertEqual(room.room_status, "Occupied")

        # check if the reservation status is one of the possible statuses
        self.assertIn(
            reservation_in_db.reservation_status,
            POSSIBLE_STATUS_AFTER_CREATION,
        )

    def test_reservation_creation_endpoint_no_room(self):
        owner_of_reservation = make_guest_in_db()

        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user=owner_of_reservation.id,
            room="",
        )

        regular_staff_token = get_regular_staff_token(self.client)
        response = self.client.post(
            CREATE_RESERVATION_URL,
            new_reservation_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
        )
        # check status code
        self.assertEqual(response.status_code, 201)

    def test_reservation_creation_endpoint_no_paymentmethod(self):
        owner_of_reservation = make_guest_in_db()
        room_available = get_room_in_db_by_status("Available")

        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="",
            user=owner_of_reservation.id,
            room=room_available.id,
        )

        regular_staff_token = get_regular_staff_token(self.client)
        response = self.client.post(
            CREATE_RESERVATION_URL,
            new_reservation_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
        )
        # check status code
        self.assertEqual(response.status_code, 201)

    def test_reservation_creation_endpoint_no_paid_amount(self):
        owner_of_reservation = make_guest_in_db()
        room_available = get_room_in_db_by_status("Available")

        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount="",
            payment_method="Credit Card",
            user=owner_of_reservation.id,
            room=room_available.id,
        )

        regular_staff_token = get_regular_staff_token(self.client)
        response = self.client.post(
            CREATE_RESERVATION_URL,
            new_reservation_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
        )
        # check status code
        self.assertEqual(response.status_code, 201)

    def test_reservation_creation_endpoint_room_not_available(self):

        room_not_available = get_room_in_db_by_status("Occupied")
        regular_staff_token = get_regular_staff_token(self.client)
        owner_of_reservation = make_guest_in_db()
        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user=owner_of_reservation.id,
            room=room_not_available.id,
        )

        response = self.client.post(
            CREATE_RESERVATION_URL,
            new_reservation_payload,
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_creation_endpoint_wrong_status(self):
        owner_of_reservation = make_guest_in_db()
        room_available = get_room_in_db_by_status("Available")
        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Wrong Status",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user=owner_of_reservation.id,
            room=room_available.id,
        )
        regular_staff_token = get_regular_staff_token(self.client)

        response = self.client.post(
            CREATE_RESERVATION_URL,
            new_reservation_payload,
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_creation_endpoint_wrong_dates(self):
        owner_of_reservation = make_guest_in_db()
        room_available = get_room_in_db_by_status("Available")
        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2021-01-02T00:00:00Z",  # wrong date
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user=owner_of_reservation.id,
            room=room_available.id,
        )
        regular_staff_token = get_regular_staff_token(self.client)
        response = self.client.post(
            CREATE_RESERVATION_URL,
            new_reservation_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_creation_endpoint_date_format_wrong(self):
        room_available = get_room_in_db_by_status("Available")
        owner_of_reservation = make_guest_in_db()
        new_reservation_payload = make_reservation_payload(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01/02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user=owner_of_reservation.id,
            room=room_available.id,
        )

        regular_staff_token = get_regular_staff_token(self.client)
        response = self.client.post(
            CREATE_RESERVATION_URL,
            new_reservation_payload,
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    # CHECKIN TESTS

    def test_reservation_checkin_endpoint(self):
        available_room = get_room_in_db_by_status("Available")
        regular_staff = make_user_in_db(
            email="regular_staff_2@example.com",
            password=DEFAULT_PASSWORD,
            role=get_role_in_db("RegularStaff"),
            username="regular staff 2",
        )

        reservation = make_reservation_in_db(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Pending",
            paid_amount="",
            payment_method="",
            user_id=regular_staff.id,
            room_id=available_room.id,
        )

        regular_staff_token = get_regular_staff_token(self.client)
        checkin_url = make_checkin_url(reservation.id)
        checkin_payload = make_checkin_payload(
            available_room.id, "Credit Card", 100.0
        )
        response = self.client.put(
            checkin_url,
            checkin_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
            content_type="application/json",
        )

        # check status code
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            TestLogger.debug(response.data)
            raise AssertionError

        # check if the room is not available anymore
        room = Reservation.objects.get(pk=reservation.id).room
        try:
            self.assertEqual(room.room_status, "Occupied")
        except AssertionError:
            TestLogger.debug(room.room_status)
            raise AssertionError

    def test_reservation_checkin_endpoint_wrong_room(self):
        occupied_room = get_room_in_db_by_status("Occupied")
        guest = make_guest_in_db()
        reservation = make_reservation_in_db(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user_id=guest.id,
            room_id=occupied_room.id,
        )
        regular_staff_token = get_regular_staff_token(self.client)
        room_occuiped = get_room_in_db_by_status("Occupied")
        checkin_url = make_checkin_url(reservation.id)

        checkin_payload = make_checkin_payload(
            room_occuiped.id, "Credit Card", 100.0
        )
        response = self.client.put(
            checkin_url,
            checkin_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
            content_type="application/json",
        )
        # check status code
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError:
            TestLogger.debug(response.data)
            raise AssertionError

    def test_reservation_checkin_endpoint_paying_already_paid(self):
        available_room = get_room_in_db_by_status("Available")
        guest = make_guest_in_db()
        reservation = make_reservation_in_db(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user_id=guest.id,
            room_id=available_room.id,
        )
        regular_staff_token = get_regular_staff_token(self.client)
        checkin_url = make_checkin_url(reservation.id)
        checkin_payload = make_checkin_payload(
            available_room.id, "Credit Card", 100.0
        )

        response = self.client.put(
            checkin_url,
            checkin_payload,
            headers={
                "Authorization": f" Bearer {regular_staff_token}",
            },
            content_type="application/json",
        )
        # check status code
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError:
            TestLogger.debug(response.data)
            raise AssertionError

    def test_reservation_checkin_endpoint_wrong_payment_method(self):
        available_room = get_room_in_db_by_status("Available")
        guest = make_guest_in_db()
        reservation = make_reservation_in_db(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Pending",
            paid_amount="",
            payment_method="",
            user_id=guest.id,
            room_id=available_room.id,
        )
        regular_staff_token = get_regular_staff_token(self.client)
        checkin_url = make_checkin_url(reservation.id)
        checkin_payload = make_checkin_payload(
            available_room.id, "Wrong Payment Method", 100.0
        )

        response = self.client.put(
            checkin_url,
            checkin_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
            content_type="application/json",
        )
        # check status code
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError:
            TestLogger.debug(response.data)
            raise AssertionError

    def test_reservation_checkin_endpoint_negative_paid_amount(self):
        available_room = get_room_in_db_by_status("Available")
        guest = make_guest_in_db()
        reservation = make_reservation_in_db(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Confirmed",
            payment_status="Pending",
            paid_amount="",
            payment_method="",
            user_id=guest.id,
            room_id=available_room.id,
        )
        regular_staff_token = get_regular_staff_token(self.client)
        checkin_url = make_checkin_url(reservation.id)
        checkin_payload = make_checkin_payload(
            available_room.id, "Credit Card", "-1000"
        )

        response = self.client.put(
            checkin_url,
            checkin_payload,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
            content_type="application/json",
        )
        # check status code
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError:
            TestLogger.debug(response.data)
            raise AssertionError

    # CHECKOUT TESTS
    def test_reservation_checkout_endpoint(self):
        available_room = get_room_in_db_by_status("Occupied")
        guest = make_guest_in_db()
        reservation = make_reservation_in_db(
            date_start="2022-01-01T00:00:00Z",
            date_end="2022-01-02T00:00:00Z",
            reservation_status="Checked In",
            payment_status="Paid",
            paid_amount=100.0,
            payment_method="Credit Card",
            user_id=guest.id,
            room_id=available_room.id,
        )
        regular_staff_token = get_regular_staff_token(self.client)
        checkout_url = make_checkout_url(reservation.id)
        response = self.client.get(
            checkout_url,
            headers={
                "Authorization": f"Bearer {regular_staff_token}",
            },
        )
        # check status code
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            TestLogger.debug(response.data)
            raise AssertionError


def test_reservation_checkout_endpoint_without_checkin(self):
    available_room = get_room_in_db_by_status("Available")
    guest = make_guest_in_db()
    reservation = make_reservation_in_db(
        self,
        date_start="2022-01-01T00:00:00Z",
        date_end="2022-01-02T00:00:00Z",
        reservation_status="Confirmed",
        payment_status="Paid",
        paid_amount=100.0,
        payment_method="Credit Card",
        guest_id=5,
        user_id=guest.id,
        room_id=available_room.id,
    )
    regular_staff_token = get_regular_staff_token(self.client)
    checkout_url = make_checkout_url(reservation.id)
    response = self.client.get(
        checkout_url,
        headers={
            "Authorization": f"Bearer {regular_staff_token}",
        },
    )
    # check status code
    try:
        self.assertEqual(response.status_code, 400)
    except AssertionError:
        TestLogger.debug(response.data)
        raise AssertionError




# TODO: Tests related to see all reservations

def test_reservation_list_endpoint(self):
    regular_staff_token = get_regular_staff_token(self.client)
    response = self.client.get(
        reverse("reservation-list"),
        headers={"Authorization": f"Bearer {regular_staff_token}"},
    )
    # check status code
    try:
        self.assertEqual(response.status_code, 200)
    except AssertionError:
        TestLogger.debug(response.data)
        raise AssertionError


def test_reservation_list_endpoint_filter_confirmed(self):
    regular_staff_token = get_regular_staff_token(self.client)
    qty_confirmed_reservations = Reservation.objects.filter(
        reservation_status="Confirmed"
    ).count()

    response = self.client.get(
        reverse("reservation-list"),
        {"reservation_status": "Confirmed"},
        headers={"Authorization": f"Bearer {regular_staff_token}"},
    )
    # check status code
    try:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), qty_confirmed_reservations)
    except AssertionError:
        TestLogger.debug(response.data)
        raise AssertionError


# TODO: Tests related to auth
