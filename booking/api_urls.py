# booking/api_urls.py
from django.urls import path
from . import api

urlpatterns = [
    path("search", api.search, name="api_search"),
    path("book", api.book, name="api_book"),
    path("bookings", api.bookings, name="api_bookings"),
    path("cancel/<str:reference>", api.cancel, name="api_cancel"),
]
