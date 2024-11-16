from rest_framework import generics
from .models import Room
from .serializers import (
    UserSerializer,
    UserStaffSerializer,
    UserCreateSerializer,
    UserGuestSerializer,
)
from core.permissions import IsManager, IsRegularStaff, IsYourself


class UserListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsRegularStaff, IsManager]


class UserDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsRegularStaff, IsManager, IsYourself]


class StaffUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = UserStaffSerializer
    permission_classes = [IsManager]


class UserStaffUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = UserStaffSerializer
    permission_classes = [IsManager]


class UserGuestUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = UserGuestSerializer
    permission_classes = [IsManager, IsYourself]


class UserStaffCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsManager]


class UserGuestCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = UserGuestSerializer
    permission_classes = [IsManager, IsRegularStaff, IsYourself]
