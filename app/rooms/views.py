from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer, RoomUpdateSerializer
from core.permissions import IsManager, IsRegularStaff, IsReservationOwner


class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsRegularStaff | IsManager]

    def get_queryset(self):
        queryset = Room.objects.all()
        room_status = self.request.query_params.get("room_status")

        if room_status is not None and room_status != "":
            queryset = queryset.filter(room_status=room_status)
        return queryset


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsRegularStaff | IsManager]


class RoomUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomUpdateSerializer
    permission_classes = [IsManager]
