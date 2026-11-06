from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Vehicle


def vehicle_list(request):

    vehicles = Vehicle.objects.all()

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    if search:
        vehicles = vehicles.filter(
            Q(vehicle_number__icontains=search) |
            Q(vehicle_name__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search)
        )

    if status:
        vehicles = vehicles.filter(status=status)

    context = {
        'vehicles': vehicles,
        'search': search,
        'selected_status': status,
    }

    return render(request, 'vehicles/vehicle_list.html', context)


def vehicle_detail(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    return render(
        request,
        'vehicles/vehicle_detail.html',
        {'vehicle': vehicle}
    )


def vehicle_create(request):

    if request.method == 'POST':

        try:
            vehicle = Vehicle(
                vehicle_number=request.POST.get('vehicle_number', '').strip().upper(),
                vehicle_name=request.POST.get('vehicle_name', '').strip(),
                vehicle_type=request.POST.get('vehicle_type'),
                brand=request.POST.get('brand', '').strip(),
                model=request.POST.get('model', '').strip(),
                year=request.POST.get('year'),
                fuel_type=request.POST.get('fuel_type'),
                capacity=request.POST.get('capacity'),
                registration_date=request.POST.get('registration_date'),
                insurance_expiry=request.POST.get('insurance_expiry'),
                status=request.POST.get('status', 'available'),
                image=request.FILES.get('image')
            )

            vehicle.full_clean()
            vehicle.save()

            messages.success(request, 'Vehicle added successfully!')
            return redirect('vehicle_list')

        except (ValidationError, ValueError, TypeError) as error:
            if hasattr(error, 'message_dict'):
                errors = error.message_dict
            elif hasattr(error, 'messages'):
                errors = {'__all__': error.messages}
            else:
                errors = {'__all__': ['Please enter valid vehicle details.']}

            return render(request, 'vehicles/vehicle_create.html', {
                'errors': errors,
                'data': request.POST,
            })

    return render(request, 'vehicles/vehicle_create.html')


def vehicle_update(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':

        try:
            vehicle.vehicle_number = request.POST.get('vehicle_number', '').strip().upper()
            vehicle.vehicle_name = request.POST.get('vehicle_name', '').strip()
            vehicle.vehicle_type = request.POST.get('vehicle_type')
            vehicle.brand = request.POST.get('brand', '').strip()
            vehicle.model = request.POST.get('model', '').strip()
            vehicle.year = request.POST.get('year')
            vehicle.fuel_type = request.POST.get('fuel_type')
            vehicle.capacity = request.POST.get('capacity')
            vehicle.registration_date = request.POST.get('registration_date')
            vehicle.insurance_expiry = request.POST.get('insurance_expiry')
            vehicle.status = request.POST.get('status')

            if request.FILES.get('image'):
                vehicle.image = request.FILES['image']

            vehicle.full_clean()
            vehicle.save()

            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vehicle_list')

        except (ValidationError, ValueError, TypeError) as error:
            if hasattr(error, 'message_dict'):
                errors = error.message_dict
            elif hasattr(error, 'messages'):
                errors = {'__all__': error.messages}
            else:
                errors = {'__all__': ['Please enter valid vehicle details.']}

            return render(request, 'vehicles/vehicle_update.html', {
                'vehicle': vehicle,
                'errors': errors,
            })

    return render(
        request,
        'vehicles/vehicle_update.html',
        {'vehicle': vehicle}
    )


def vehicle_delete(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':

        vehicle.delete()

        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('vehicle_list')

    return render(
        request,
        'vehicles/vehicle_delete.html',
        {'vehicle': vehicle}
    )
