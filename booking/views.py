from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SearchForm, BookingForm
from .models import Trip, Booking, BookingEvent


def search(request):
    form = SearchForm(request.GET or None)
    qs = Trip.objects.all()

    if form.is_valid():
        origin = form.cleaned_data.get('origin')
        destination = form.cleaned_data.get('destination')
        depart_date = form.cleaned_data.get('depart_date')
        return_date = form.cleaned_data.get('return_date')
        if origin:
            qs = qs.filter(origin__icontains=origin)
        if destination:
            qs = qs.filter(destination__icontains=destination)
        if depart_date:
            qs = qs.filter(depart_date=depart_date)
        if return_date:
            qs = qs.filter(return_date=return_date)

    trips = qs.order_by('depart_date')[:100]
    return render(request, 'booking/search_results.html', {'form': form, 'trips': trips})


@login_required
@transaction.atomic
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            passengers = form.cleaned_data['passengers']
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']

            if not trip.reserve_seats(passengers):
                messages.error(request, 'Sorry, not enough seats left for this trip.')
                return redirect('booking:book', trip_id=trip.id)

            total = trip.price_eur * passengers
            booking = Booking.objects.create(
                user=request.user,
                trip=trip,
                passengers=passengers,
                contact_name=contact_name,
                contact_email=contact_email,
                total_price_eur=total,
                status=Booking.Status.CONFIRMED,
            )
            BookingEvent.objects.create(
                booking=booking,
                kind=BookingEvent.Kind.CREATED,
                note='Booking confirmed'
            )

            messages.success(request, f'Booking confirmed! Reference: {booking.reference}')
            return redirect('booking:success', reference=booking.reference)
    else:
        form = BookingForm(initial={'passengers': int(request.GET.get('travellers', 1))})

    return render(request, 'booking/book_trip.html', {'trip': trip, 'form': form})


@login_required
def booking_success(request, reference):
    booking = get_object_or_404(Booking, reference=reference, user=request.user)
    return render(request, 'booking/booking_success.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related('trip')
        .prefetch_related('events')
        .order_by('-created_at')
    )
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
@transaction.atomic
def cancel_booking(request, reference):
    booking = get_object_or_404(Booking, reference=reference, user=request.user)
    if booking.status == Booking.Status.CANCELLED:
        messages.info(request, 'This booking is already cancelled.')
        return redirect('booking:my_bookings')

    booking.trip.release_seats(booking.passengers)
    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=['status', 'updated_at'])
    BookingEvent.objects.create(
        booking=booking,
        kind=BookingEvent.Kind.CANCELLED,
        note='Cancelled by user'
    )

    messages.success(request, 'Your booking has been cancelled and seats were released.')
    return redirect('booking:my_bookings')

