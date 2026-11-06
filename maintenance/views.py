from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Maintenance
from vehicles.models import Vehicle


@login_required
def maintenance_list(request):
    records = Maintenance.objects.select_related('vehicle').order_by('-service_date')
    return render(request, 'maintenance/maintenance_list.html', {'records': records})


@login_required
def maintenance_detail(request, pk):
    record = get_object_or_404(Maintenance, pk=pk)
    return render(request, 'maintenance/maintenance_detail.html', {'record': record})


@login_required
def maintenance_create(request):
    if request.method == 'POST':
        try:
            Maintenance.objects.create(
                vehicle_id=request.POST.get('vehicle'),
                maintenance_type=request.POST.get('maintenance_type'),
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                service_date=request.POST.get('service_date'),
                next_service_date=request.POST.get('next_service_date') or None,
                odometer_reading=request.POST.get('odometer_reading'),
                service_center=request.POST.get('service_center'),
                cost=request.POST.get('cost'),
                status=request.POST.get('status', 'scheduled'),
                performed_by=request.user
            )
            messages.success(request, 'Maintenance record created.')
            return redirect('maintenance_list')
        except Exception as e:
            messages.error(request, f'Unable to create record: {e}')

    return render(request, 'maintenance/maintenance_create.html', {
        'vehicles': Vehicle.objects.all()
    })


@login_required
def maintenance_update(request, pk):
    record = get_object_or_404(Maintenance, pk=pk)

    if request.method == 'POST':
        try:
            record.vehicle_id = request.POST.get('vehicle')
            record.maintenance_type = request.POST.get('maintenance_type')
            record.title = request.POST.get('title')
            record.description = request.POST.get('description')
            record.service_date = request.POST.get('service_date')
            record.next_service_date = request.POST.get('next_service_date') or None
            record.odometer_reading = request.POST.get('odometer_reading')
            record.service_center = request.POST.get('service_center')
            record.cost = request.POST.get('cost')
            record.status = request.POST.get('status')
            record.save()

            messages.success(request, 'Maintenance record updated.')
            return redirect('maintenance_list')
        except Exception as e:
            messages.error(request, f'Unable to update record: {e}')

    return render(request, 'maintenance/maintenance_update.html', {
        'record': record,
        'vehicles': Vehicle.objects.all()
    })
