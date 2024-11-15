from rest_framework import permissions
from reservations.models import Reservation


class IsRegularStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        # should not be annonymous user
        if request.user.is_anonymous:
            return False

        if request.user.role and request.user.role.name == "RegularStaff":
            return True
        return False


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        # should not be annonymous user
        if request.user.is_anonymous:
            return False

        if request.user.role and request.user.role.name == "ManagerStaff":
            return True
        return False


class IsGuest(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        # should not be annonymous user
        if request.user.is_anonymous:
            return False

        if request.user.role and request.user.role.name == "Guest":
            return True
        return False


class IsReservationOwner(permissions.BasePermission):
    pass
