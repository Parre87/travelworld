from django.db import models
from django.utils.crypto import get_random_string

class Booking(models.Model):
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = [(STATUS_CONFIRMED, "CONFIRMED"), (STATUS_CANCELLED, "CANCELLED")]

    reference = models.CharField(max_length=32, unique=True, editable=False)
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    depart_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    travellers = models.PositiveIntegerField(default=1)
    total_eur = models.DecimalField(max_digits=10, decimal_places=2)
    contact_name = models.CharField(max_length=80)
    contact_email = models.EmailField(max_length=120)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_CONFIRMED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_reference():
        return "TRV-" + get_random_string(8).upper()

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} {self.origin}→{self.destination}"

class BookingEvent(models.Model):
    booking = models.ForeignKey(Booking, related_name="events", on_delete=models.CASCADE)
    kind = models.CharField(max_length=32)  # e.g. CREATED, CANCELLED
    note = models.CharField(max_length=200, blank=True)
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-at"]

    def __str__(self):
        return f"{self.booking.reference} {self.kind}"
