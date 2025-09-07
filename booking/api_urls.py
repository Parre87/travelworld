from django.urls import path
from . import api

urlpatterns = [
    path("search", api.search, name="api_search"),
    path("book", api.book, name="api_book"),
    path("bookings", api.list_bookings, name="api_bookings"),  # <-- rätt namn här
    path("booking/<str:reference>", api.get_booking, name="api_get_booking"),
    path("booking/<str:reference>/cancel", api.cancel_booking, name="api_cancel_booking"),
]
