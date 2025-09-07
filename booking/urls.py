# booking/urls.py
from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("book/<int:trip_id>/", views.book_trip, name="book"),
    path("booking/<str:reference>/success/", views.booking_success, name="success"),
    path("my/bookings/", views.my_bookings, name="my_bookings"),
    path("booking/<str:reference>/cancel/", views.cancel_booking, name="cancel"),
]
