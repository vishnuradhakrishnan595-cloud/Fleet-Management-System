from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from .models import Trip
from vehicles.models import Vehicle
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def trip_list(request):
    trips = Trip.objects.select_related('vehicle', 'driver').all().order_by('-created_at')
    return render(request, 'trips/trip_list.html', {'trips': trips})


@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'trips/trip_detail.html', {'trip': trip})


@login_required
def trip_create(request):
    vehicles = Vehicle.objects.all()
    drivers = User.objects.filter(role='driver')

    if request.method == 'POST':
        try:
            start_date = parse_datetime(request.POST.get('start_date'))
            end_date = parse_datetime(request.POST.get('end_date') or '') or None

            trip = Trip.objects.create(
                vehicle_id=request.POST.get('vehicle'),
                driver_id=request.POST.get('driver'),
                start_location=request.POST.get('start_location'),
                destination=request.POST.get('destination'),
                start_date=start_date,
                end_date=end_date,
                starting_odometer=request.POST.get('starting_odometer'),
                ending_odometer=request.POST.get('ending_odometer') or None,
                purpose=request.POST.get('purpose', ''),
                status=request.POST.get('status', 'scheduled'),
                notes=request.POST.get('notes', '')
            )

            messages.success(request, 'Trip created successfully.')
            return redirect('trip_detail', pk=trip.pk)

        except (ValueError, TypeError, Exception) as e:
            messages.error(request, f'Unable to create trip: {e}')

    return render(request, 'trips/trip_create.html', {
        'vehicles': vehicles,
        'drivers': drivers
    })


@login_required
def trip_update(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == 'POST':
        try:
            trip.vehicle_id = request.POST.get('vehicle')
            trip.driver_id = request.POST.get('driver')
            trip.start_location = request.POST.get('start_location')
            trip.destination = request.POST.get('destination')
            trip.start_date = parse_datetime(request.POST.get('start_date'))
            trip.end_date = parse_datetime(request.POST.get('end_date') or '') or None
            trip.starting_odometer = request.POST.get('starting_odometer')
            trip.ending_odometer = request.POST.get('ending_odometer') or None
            trip.purpose = request.POST.get('purpose', '')
            trip.status = request.POST.get('status')
            trip.notes = request.POST.get('notes', '')
            trip.save()

            messages.success(request, 'Trip updated successfully.')
            return redirect('trip_detail', pk=trip.pk)

        except Exception as e:
            messages.error(request, f'Unable to update trip: {e}')

    return render(request, 'trips/trip_update.html', {
        'trip': trip,
        'vehicles': Vehicle.objects.all(),
        'drivers': User.objects.filter(role='driver')
    })


@login_required
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Trip deleted successfully.')
        return redirect('trip_list')

    return render(request, 'trips/trip_delete.html', {'trip': trip})
