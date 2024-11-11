from django.urls import path
from . import views

urlpatterns = [
    path("", views.ReservationListView.as_view(), name="reservation-list"),
    path(
        "create/",
        views.ReservationCreateView.as_view(),
        name="reservation-create",
    ),
    # path(
    #     "<int:pk>/",
    #     views.ReservationDetailView.as_view(),
    #     name="reservation-detail",
    # ),
    # path(
    #     "<int:pk>/update/",
    #     views.ReservationUpdateView.as_view(),
    #     name="reservation-update",
    # ),
    path(
        "<int:pk>/update/checkin",
        views.ReservationUpdateCheckinView.as_view(),
        name="reservation-update-checkin",
    ),
    # path("<int:pk>/", views.RoomDetailView.as_view(), name="reservation-detail"),
]
