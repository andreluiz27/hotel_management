from rest_framework import generics
from core.permissions import IsRegularStaff, IsManager, IsReservationOwner
import django_filters.rest_framework

from .serializers import (
    ReservationSerializer,
    CreateReservationSerializer,
    ReservationUpdateCheckinSerializer,
    ReservationUpdateCheckoutSerializer,
)
from .models import Reservation
from rooms.models import Room


class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = (IsRegularStaff | IsManager,)
    filterset_fields = {
        "reservation_status": ["exact"],
        "guest": ["exact"],
    }

    def get_queryset(self):
        queryset = Reservation.objects.all()
        reservation_status = self.request.query_params.get(
            "reservation_status"
        )
        guest = self.request.query_params.get("guest")

        if reservation_status is not None and reservation_status != "":
            queryset = queryset.filter(reservation_status=reservation_status)

        if guest is not None and guest != "":
            queryset = queryset.filter(guest=guest)
        return queryset


class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = CreateReservationSerializer
    permission_classes = [IsRegularStaff | IsManager]


class ReservationUpdateCheckinView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationUpdateCheckinSerializer
    permission_classes = [IsRegularStaff | IsManager]


class ReservationUpdateCheckoutView(generics.RetrieveUpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationUpdateCheckoutSerializer
    permission_classes = [IsRegularStaff | IsManager]


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsRegularStaff | IsManager | IsReservationOwner]
