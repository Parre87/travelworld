# booking/api.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.utils.dateparse import parse_date
from django.db import transaction
from .models import Trip, Booking, BookingEvent
import json

def _auth_or_401(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"detail": "auth_required", "login_url": f"/accounts/login/?next={request.path}"},
            status=401
        )
    return None

@require_GET
def search(request):
    origin = request.GET.get("from") or request.GET.get("origin")
    destination = request.GET.get("to") or request.GET.get("destination")
    depart = parse_date(request.GET.get("depart") or "")
    ret = parse_date(request.GET.get("return") or "")

    qs = Trip.objects.all()
    if origin: qs = qs.filter(origin__icontains=origin)
    if destination: qs = qs.filter(destination__icontains=destination)
    if depart: qs = qs.filter(depart_date=depart)
    if ret: qs = qs.filter(return_date=ret)

    trips = list(qs.order_by("depart_date")[:50].values(
        "id","origin","destination","depart_date","return_date","price_eur","seats_available"
    ))
    return JsonResponse({"trips": trips})

@require_GET
def bookings(request):
    err = _auth_or_401(request)
    if err: return err

    qs = (Booking.objects
          .filter(user=request.user)
          .select_related("trip")
          .order_by("-created_at"))

    data = [{
        "reference": b.reference,
        "status": b.status,
        "created_at": b.created_at.isoformat(),
        "origin": b.trip.origin,
        "destination": b.trip.destination,
        "depart": b.trip.depart_date.isoformat(),
        "return": b.trip.return_date.isoformat() if b.trip.return_date else None,
        "travellers": b.passengers,
        "total": float(b.total_price_eur),
    } for b in qs]

    return JsonResponse({"bookings": data})

@require_POST
@transaction.atomic
def book(request):
    err = _auth_or_401(request)
    if err: return err

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "invalid_json"}, status=400)

    trip = get_object_or_404(Trip, pk=data.get("trip_id"))
    passengers = int(data.get("passengers") or 1)
    name = (data.get("contact_name") or "").strip()
    email = (data.get("contact_email") or "").strip()

    if not name or not email:
        return JsonResponse({"detail": "missing_contact"}, status=400)
    if passengers < 1:
        return JsonResponse({"detail": "invalid_passengers"}, status=400)

    if not trip.reserve_seats(passengers):
        return JsonResponse({"detail": "not_enough_seats"}, status=400)

    total = trip.price_eur * passengers
    booking = Booking.objects.create(
        user=request.user,
        trip=trip,
        passengers=passengers,
        contact_name=name,
        contact_email=email,
        total_price_eur=total,
        status=Booking.Status.CONFIRMED,
    )
    BookingEvent.objects.create(
        booking=booking,
        kind=BookingEvent.Kind.CREATED,
        note="Booking confirmed"
    )

    return JsonResponse({"reference": booking.reference, "total": float(total)})

@require_POST
@transaction.atomic
def cancel(request, reference):
    err = _auth_or_401(request)
    if err: return err

    b = get_object_or_404(Booking, reference=reference, user=request.user)
    if b.status == Booking.Status.CANCELLED:
        return JsonResponse({"detail": "already_cancelled"})

    b.trip.release_seats(b.passengers)
    b.status = Booking.Status.CANCELLED
    b.save(update_fields=["status", "updated_at"])
    BookingEvent.objects.create(
        booking=b,
        kind=BookingEvent.Kind.CANCELLED,
        note="Cancelled by user"
    )
    return JsonResponse({"detail": "cancelled"})
