from rest_framework import generics, permissions
import django_filters.rest_framework

from .serializers import (
    ReservationSerializer,
    CreateReservationSerializer,
    ReservationUpdateCheckinSerializer,
)
from .models import Reservation


class ReservationListView(generics.ListAPIView):
    # queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

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


class ReservationUpdateCheckinView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationUpdateCheckinSerializer

# class RoomListView(generics.ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [permissions.AllowAny]


# class RoomDetailView(generics.RetrieveAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [permissions.AllowAny]


# class RoomUpdateView(generics.UpdateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomUpdateSerializer
#     permission_classes = [permissions.IsAuthenticated]
