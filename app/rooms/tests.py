from django.test import TestCase
from helpers_tests import (
    get_role_in_db,
    make_user_in_db,
    make_guest_in_db,
    make_reservation_in_db,
    make_random_username,
    make_random_email,
    DEFAULT_PASSWORD,
    get_token,
    get_manager_staff_token,
    get_regular_staff_token,
    get_guest_token,
    get_room_in_db_by_status,
)
import logging
from django.urls import reverse
from core.settings import TEST_LOGGER_LEVEL
from .models import Room

logging.basicConfig(
    level=TEST_LOGGER_LEVEL, format="%(message)s - %(asctime)s"
)

TestLogger = logging.getLogger(__name__)

LIST_ROOMS_ENDPOINT = reverse("room-list")
DETAIL_ROOM_ENDPOINT = reverse("room-detail", args=[1])


class RoomTestCase(TestCase):
    fixtures = ["initial_test_data.json"]

    def test_room_list_endpoint(self):
        regular_staff_token = get_regular_staff_token(self.client)
        response = self.client.get(
            LIST_ROOMS_ENDPOINT,
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )

        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    def test_room_list_endpoint_filter_occupied(self):
        regular_staff_token = get_regular_staff_token(self.client)
        qty_occupied_rooms = Room.objects.filter(
            room_status="Occupied"
        ).count()

        response = self.client.get(
            LIST_ROOMS_ENDPOINT,
            {"room_status": "Occupied"},
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), qty_occupied_rooms)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    def test_room_list_endpoint_filter_available(self):
        regular_staff_token = get_regular_staff_token(self.client)
        qty_available_rooms = Room.objects.filter(
            room_status="Available"
        ).count()

        response = self.client.get(
            LIST_ROOMS_ENDPOINT,
            {"room_status": "Available"},
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), qty_available_rooms)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    def test_room_detail_endpoint(self):
        regular_staff_token = get_regular_staff_token(self.client)
        room = get_room_in_db_by_status("Available")
        response = self.client.get(
            reverse("room-detail", args=[room.id]),
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )

        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    def test_room_list_endpoint_filter_cleaning(self):
        regular_staff_token = get_regular_staff_token(self.client)
        qty_cleaning_rooms = Room.objects.filter(
            room_status="Cleaning"
        ).count()

        response = self.client.get(
            LIST_ROOMS_ENDPOINT,
            {"room_status": "Cleaning"},
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), qty_cleaning_rooms)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    def test_room_list_endpoint_filter_maintenance(self):
        regular_staff_token = get_regular_staff_token(self.client)
        qty_maintenance_rooms = Room.objects.filter(
            room_status="Maintenance"
        ).count()

        response = self.client.get(
            LIST_ROOMS_ENDPOINT,
            {"room_status": "Maintenance"},
            headers={"Authorization": f"Bearer {regular_staff_token}"},
        )

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), qty_maintenance_rooms)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    # AUTHORIZATION TESTS
    def test_room_list_endpoint_manage_can_see(self):
        manager_staff_token = get_manager_staff_token(self.client)
        response = self.client.get(
            LIST_ROOMS_ENDPOINT,
            headers={"Authorization": f"Bearer {manager_staff_token}"},
        )
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    def test_room_list_endpoint_unauthorized(self):
        response = self.client.get(LIST_ROOMS_ENDPOINT)

        try:
            self.assertEqual(response.status_code, 401)
        except AssertionError as e:
            TestLogger.error(e)
            raise

    def test_room_list_endpoint_unauthorized_user(self):
        guest_token = get_guest_token(self.client)
        response = self.client.get(
            LIST_ROOMS_ENDPOINT,
            headers={"Authorization": f"Bearer {guest_token}"},
        )

        try:
            self.assertEqual(response.status_code, 403)
        except AssertionError as e:
            TestLogger.error(e)
            raise
