from __future__ import annotations
from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
import uuid

class Trip(models.Model):
    ORIGIN_MAX = 64
    DEST_MAX = 64

    origin = models.CharField(max_length=ORIGIN_MAX)
    destination = models.CharField(max_length=DEST_MAX)
    depart_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    price_eur = models.DecimalField(max_digits=10, decimal_places=2)
    seats_available = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['depart_date', 'origin', 'destination']
        indexes = [
            models.Index(fields=['origin', 'destination', 'depart_date'])
        ]

    def __str__(self) -> str:
        r = f" → {self.destination}"
        if self.return_date:
            r += f" (return {self.return_date})"
        return f"{self.origin}{r} on {self.depart_date} — €{self.price_eur} ({self.seats_available} seats)"

    @transaction.atomic
    def reserve_seats(self, count: int) -> bool:
        trip = Trip.objects.select_for_update().get(pk=self.pk)
        if trip.seats_available < count:
            return False
        trip.seats_available -= count
        trip.save(update_fields=['seats_available'])
        return True

    @transaction.atomic
    def release_seats(self, count: int) -> None:
        trip = Trip.objects.select_for_update().get(pk=self.pk)
        trip.seats_available += count
        trip.save(update_fields=['seats_available'])


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, related_name='bookings')

    reference = models.CharField(max_length=14, unique=True, editable=False)
    passengers = models.PositiveIntegerField(default=1)

    contact_name = models.CharField(max_length=120)
    contact_email = models.EmailField()

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.CONFIRMED)

    total_price_eur = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.reference} — {self.user} — {self.trip}"

    def save(self, *args, **kwargs):
        # 👇 THIS BLOCK MUST BE INDENTED UNDER THE METHOD
        if not self.reference:
            # short unique ref like TRV-ABC1234
            token = uuid.uuid4().hex[:7].upper()
            self.reference = f"TRV-{token}"
        super().save(*args, **kwargs)


class BookingEvent(models.Model):
    class Kind(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        CANCELLED = 'CANCELLED', 'Cancelled'
        UPDATED = 'UPDATED', 'Updated'

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='events')
    kind = models.CharField(max_length=12, choices=Kind.choices)
    note = models.TextField(blank=True)
    at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-at']

    def __str__(self) -> str:
        return f"{self.at:%Y-%m-%d %H:%M} — {self.kind}"
