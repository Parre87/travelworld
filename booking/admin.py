from django.contrib import admin
from .models import Trip, Booking, BookingEvent


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "depart_date", "return_date", "price_eur", "seats_available")
    list_filter = ("origin", "destination", "depart_date")
    search_fields = ("origin", "destination")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference", "user", "trip", "passengers", "status", "total_price_eur", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("reference", "user__username", "trip__origin", "trip__destination")


@admin.register(BookingEvent)
class BookingEventAdmin(admin.ModelAdmin):
    list_display = ("booking", "kind", "at", "note")
    list_filter = ("kind", "at")
