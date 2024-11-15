from django.urls import path
from . import views

urlpatterns = [
    path("", views.ReservationListView.as_view(), name="reservation-list"),
    path(
        "create/",
        views.ReservationCreateView.as_view(),
        name="reservation-create",
    ),
    path(
        "<int:pk>/update/checkin",
        views.ReservationUpdateCheckinView.as_view(),
        name="reservation-update-checkin",
    ),
    path(
        "<int:pk>/update/checkout",
        views.ReservationUpdateCheckoutView.as_view(),
        name="reservation-update-checkout",
    ),
]
