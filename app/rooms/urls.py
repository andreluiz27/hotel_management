from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomListView.as_view(), name="room-list"),
    path("<int:pk>/", views.RoomDetailView.as_view(), name="room-detail"),
    path(
        "<int:pk>/update/", views.RoomUpdateView.as_view(), name="room-update"
    ),
]
