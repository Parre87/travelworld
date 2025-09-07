from django.contrib import admin
from .models import Booking, BookingEvent

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference","origin","destination","depart_date","return_date","travellers","total_eur","status","created_at")
    search_fields = ("reference","origin","destination","contact_email","contact_name")
    list_filter = ("status","depart_date","created_at")

@admin.register(BookingEvent)
class BookingEventAdmin(admin.ModelAdmin):
    list_display = ("booking","kind","at","note")
    list_filter = ("kind",)
