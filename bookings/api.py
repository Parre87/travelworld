import json
from decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils.dateparse import parse_date
from .models import Booking, BookingEvent

# En enkel "prislista" för demo
CITY_PRICE = {
    "Paris": 129, "Tokyo": 499, "New": 399, "Maldives": 799,
    "London": 159, "Rome": 139, "Barcelona": 129, "Berlin": 119,
}

def _serialize_booking(b: Booking):
    return {
        "reference": b.reference,
        "status": b.status,
        "created_at": b.created_at.isoformat(),
        "origin": b.origin,
        "destination": b.destination,
        "depart": b.depart_date.isoformat(),
        "return": b.return_date.isoformat() if b.return_date else None,
        "travellers": b.travellers,
        "total_eur": float(b.total_eur),
        "contact_name": b.contact_name,
        "contact_email": b.contact_email,
        "events": [
            {"kind": e.kind, "note": e.note, "at": e.at.isoformat()}
            for e in b.events.all()
        ],
    }

@require_GET
def search(request):
    origin = (request.GET.get("from") or request.GET.get("origin") or "").strip()
    dest = (request.GET.get("to") or request.GET.get("destination") or "").strip()
    depart = request.GET.get("depart")
    ret = request.GET.get("return") or None
    travellers = int(request.GET.get("travellers") or 1)

    if not origin or not dest or not depart:
        return HttpResponseBadRequest("Missing required fields: from, to, depart")

    dest_key = dest.split()[0].strip(" ,(")
    base = CITY_PRICE.get(dest_key, 199)
    total = max(49, base) * max(1, travellers)

    result = {
        "origin": origin, "destination": dest, "depart": depart,
        "return": ret, "travellers": travellers, "total_eur": total
    }
    return JsonResponse({"results": [result]})

@require_GET
def list_bookings(request):
    qs = Booking.objects.order_by("-created_at").prefetch_related("events")
    return JsonResponse({"items": [_serialize_booking(b) for b in qs]})

@require_GET
def get_booking(request, reference: str):
    try:
        b = Booking.objects.prefetch_related("events").get(reference=reference)
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse(_serialize_booking(b))

@require_POST
@csrf_protect
def book(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = request.POST.dict()

    required = ["origin","destination","depart","travellers","total_eur","contact_name","contact_email"]
    if any(k not in data or not str(data[k]).strip() for k in required):
        return HttpResponseBadRequest("Missing booking fields")

    depart_date = parse_date(data["depart"])
    return_date = parse_date(data.get("return")) if data.get("return") else None
    if not depart_date:
        return HttpResponseBadRequest("Invalid depart date")
    if return_date and return_date < depart_date:
        return HttpResponseBadRequest("Return date cannot be before depart date")

    travellers = max(1, int(data.get("travellers", 1)))
    total_eur = Decimal(str(data.get("total_eur", "0")))

    b = Booking.objects.create(
        origin=data["origin"].strip(),
        destination=data["destination"].strip(),
        depart_date=depart_date,
        return_date=return_date,
        travellers=travellers,
        total_eur=total_eur,
        contact_name=data["contact_name"].strip(),
        contact_email=data["contact_email"].strip(),
    )
    BookingEvent.objects.create(booking=b, kind="CREATED", note="Booking confirmed")

    return JsonResponse(_serialize_booking(b), status=201)

@require_POST
@csrf_protect
def cancel_booking(request, reference: str):
    try:
        b = Booking.objects.get(reference=reference)
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    if b.status != Booking.STATUS_CANCELLED:
        b.status = Booking.STATUS_CANCELLED
        b.save(update_fields=["status", "updated_at"])
        BookingEvent.objects.create(booking=b, kind="CANCELLED", note="Cancelled by user")
    return JsonResponse({"ok": True, "booking": _serialize_booking(b)})
