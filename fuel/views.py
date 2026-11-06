from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FuelRecord
from vehicles.models import Vehicle


@login_required
def fuel_list(request):
    records = FuelRecord.objects.select_related('vehicle').order_by('-fuel_date')
    return render(request, 'fuel/fuel_list.html', {'records': records})


@login_required
def fuel_detail(request, pk):
    record = get_object_or_404(FuelRecord, pk=pk)
    return render(request, 'fuel/fuel_detail.html', {'record': record})


@login_required
def fuel_create(request):
    if request.method == 'POST':
        try:
            record = FuelRecord(
                vehicle_id=request.POST.get('vehicle'),
                driver=request.user,
                fuel_type=request.POST.get('fuel_type'),
                quantity=request.POST.get('quantity'),
                price_per_unit=request.POST.get('price_per_unit'),
                odometer_reading=request.POST.get('odometer_reading'),
                fuel_date=request.POST.get('fuel_date'),
                station_name=request.POST.get('station_name', ''),
                receipt=request.FILES.get('receipt'),
                notes=request.POST.get('notes', '')
            )
            record.save()
            messages.success(request, 'Fuel record created.')
            return redirect('fuel_list')
        except Exception as e:
            messages.error(request, f'Unable to save fuel record: {e}')

    return render(request, 'fuel/fuel_create.html', {
        'vehicles': Vehicle.objects.all()
    })


@login_required
def fuel_update(request, pk):
    record = get_object_or_404(FuelRecord, pk=pk)

    if request.method == 'POST':
        try:
            record.vehicle_id = request.POST.get('vehicle')
            record.fuel_type = request.POST.get('fuel_type')
            record.quantity = request.POST.get('quantity')
            record.price_per_unit = request.POST.get('price_per_unit')
            record.odometer_reading = request.POST.get('odometer_reading')
            record.fuel_date = request.POST.get('fuel_date')
            record.station_name = request.POST.get('station_name', '')
            record.notes = request.POST.get('notes', '')

            if request.FILES.get('receipt'):
                record.receipt = request.FILES['receipt']

            record.save()
            messages.success(request, 'Fuel record updated.')
            return redirect('fuel_list')
        except Exception as e:
            messages.error(request, f'Unable to update record: {e}')

    return render(request, 'fuel/fuel_update.html', {
        'record': record,
        'vehicles': Vehicle.objects.all()
    })
