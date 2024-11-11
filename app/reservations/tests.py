from django.test import TestCase
from django.urls import reverse
from .models import Reservation


# CONSTANTS
AVAILABLE_ROOM_ID = 103
NOT_AVAILABLE_ROOM_ID = 101
POSSIBLE_STATUS_AFTER_CREATION = ["Confirmed", "On Hold"]
RESERVATION_ID = 5
AVAILABLE_ROOM_ID = 302


# PAYLOADS
NEW_RESERVATION_PAYLOAD = {
    "date_start": "2022-01-01T00:00:00Z",
    "date_end": "2022-01-02T00:00:00Z",
    "reservation_status": "Confirmed",
    "payment_status": "Paid",
    "paid_amount": 100.0,
    "payment_method": "Credit Card",
    "guest": 1,
    "staff": 1,
    "room": AVAILABLE_ROOM_ID,
}

# URLS
CREATE_RESERVATION_URL = reverse("reservation-create")
CHECKIN_RESERVATION_URL = reverse(
    "reservation-update-checkin", args=[RESERVATION_ID]
)
CHECKIN_RESERVATION_PAYLOAD = {
    "room": AVAILABLE_ROOM_ID,
    "payment_method": "Credit Card",
    "paid_amount": 100.0,
}

# TEST CASES


class ReservationTestCase(TestCase):
    fixtures = ["initial_test_data.json"]

    def test_reservation_creation_endpoint(self):
        response = self.client.post(
            CREATE_RESERVATION_URL, NEW_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 201)

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
        NEW_RESERVATION_PAYLOAD.pop("room")
        response = self.client.post(
            CREATE_RESERVATION_URL, NEW_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 201)

    def test_reservation_creation_endpoint_no_paymentmethod(self):
        NEW_RESERVATION_PAYLOAD.pop("payment_method")
        response = self.client.post(
            CREATE_RESERVATION_URL, NEW_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 201)

    def test_reservation_creation_endpoint_no_paid_amount(self):
        NEW_RESERVATION_PAYLOAD.pop("paid_amount")
        response = self.client.post(
            CREATE_RESERVATION_URL, NEW_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 201)

    def test_reservation_creation_endpoint_room_not_available(self):
        WRONG_ROOM_RESERVATION_PAYLOAD = NEW_RESERVATION_PAYLOAD.copy()
        WRONG_ROOM_RESERVATION_PAYLOAD["room"] = NOT_AVAILABLE_ROOM_ID
        response = self.client.post(
            CREATE_RESERVATION_URL, WRONG_ROOM_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_creation_endpoint_wrong_status(self):
        WRONG_STATUS_RESERVATION_PAYLOAD = NEW_RESERVATION_PAYLOAD.copy()
        WRONG_STATUS_RESERVATION_PAYLOAD["reservation_status"] = "Wrong Status"

        response = self.client.post(
            CREATE_RESERVATION_URL, WRONG_STATUS_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_creation_endpoint_wrong_dates(self):
        WRONG_DATES_RESERVATION_PAYLOAD = NEW_RESERVATION_PAYLOAD.copy()
        WRONG_DATES_RESERVATION_PAYLOAD["date_start"] = (
            "2022-01-03T00:00:00Z"  # start date after end date
        )
        response = self.client.post(
            CREATE_RESERVATION_URL, WRONG_DATES_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_creation_endpoint_date_format_wrong(self):
        WRONG_DATE_FORMAT_RESERVATION_PAYLOAD = NEW_RESERVATION_PAYLOAD.copy()
        WRONG_DATE_FORMAT_RESERVATION_PAYLOAD["date_start"] = (
            "2022/01-01"  # wrong date format
        )
        response = self.client.post(
            CREATE_RESERVATION_URL, WRONG_DATE_FORMAT_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_checkin_endpoint(self):
        response = self.client.put(
            CHECKIN_RESERVATION_URL,
            CHECKIN_RESERVATION_PAYLOAD,
            headers={"Content-Type": "application/json"},
        )
        # check status code
        self.assertEqual(response.status_code, 200)

        print(response.data)

        # check if the room is not available anymore
        reservation_in_db = Reservation.objects.get(pk=1)
        room = reservation_in_db.room
        self.assertEqual(room.room_status, "Occupied")

    def test_reservation_checkin_endpoint_room_needed(self):
        # reservation has no room previously so checkin needs a room

        reservation_in_db = Reservation.objects.get(pk=1)
        reservation_in_db.room = None

        response = self.client.put(
            CHECKIN_RESERVATION_URL, CHECKIN_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_checkin_endpoint_no_room(self):
        CHECKIN_RESERVATION_PAYLOAD.pop("room")
        response = self.client.patch(
            CHECKIN_RESERVATION_URL, CHECKIN_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 200)

    def test_reservation_checkin_endpoint_no_paymentmethod(self):
        CHECKIN_RESERVATION_PAYLOAD.pop("payment_method")
        response = self.client.patch(
            CHECKIN_RESERVATION_URL, CHECKIN_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 400)

    def test_reservation_checkin_endpoint_no_paid_amount(self):
        CHECKIN_RESERVATION_PAYLOAD.pop("paid_amount")
        response = self.client.put(
            CHECKIN_RESERVATION_URL, CHECKIN_RESERVATION_PAYLOAD
        )
        # check status code
        self.assertEqual(response.status_code, 400)
