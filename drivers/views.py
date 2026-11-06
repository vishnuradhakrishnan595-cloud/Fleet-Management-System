from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError

from .models import Driver


def driver_list(request):

    search = request.GET.get('search', '')

    drivers = Driver.objects.all()

    if search:
        drivers = drivers.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(license_number__icontains=search)
        )

    context = {
        'drivers': drivers,
        'search': search,
        'total_drivers': Driver.objects.count(),
    }

    return render(
        request,
        'drivers/driver_list.html',
        context
    )


def driver_detail(request, pk):

    driver = get_object_or_404(Driver, pk=pk)

    return render(
        request,
        'drivers/driver_detail.html',
        {'driver': driver}
    )


def driver_create(request):

    if request.method == 'POST':

        driver = Driver(
            employee_id=request.POST.get('employee_id', '').strip(),
            first_name=request.POST.get('first_name', '').strip(),
            last_name=request.POST.get('last_name', '').strip(),
            email=request.POST.get('email', '').strip(),
            phone=request.POST.get('phone', '').strip(),
            license_number=request.POST.get('license_number', '').strip(),
            license_type=request.POST.get('license_type', ''),
            license_expiry=request.POST.get('license_expiry', ''),
            date_of_joining=request.POST.get('date_of_joining', ''),
            address=request.POST.get('address', '').strip(),
            status=request.POST.get('status', 'available'),
        )

        try:
            driver.full_clean()
            driver.save()

            messages.success(request, 'Driver added successfully!')
            return redirect('driver_list')

        except ValidationError as error:
            if hasattr(error, 'message_dict'):
                for field_errors in error.message_dict.values():
                    for error_message in field_errors:
                        messages.error(request, error_message)
            else:
                for error_message in error.messages:
                    messages.error(request, error_message)

    return render(
        request,
        'drivers/driver_create.html'
    )


def driver_update(request, pk):

    driver = get_object_or_404(Driver, pk=pk)

    if request.method == 'POST':

        driver.employee_id = request.POST.get('employee_id', '').strip()
        driver.first_name = request.POST.get('first_name', '').strip()
        driver.last_name = request.POST.get('last_name', '').strip()
        driver.email = request.POST.get('email', '').strip()
        driver.phone = request.POST.get('phone', '').strip()
        driver.license_number = request.POST.get('license_number', '').strip()
        driver.license_type = request.POST.get('license_type', '')
        driver.license_expiry = request.POST.get('license_expiry', '')
        driver.date_of_joining = request.POST.get('date_of_joining', '')
        driver.address = request.POST.get('address', '').strip()
        driver.status = request.POST.get('status', 'available')

        try:
            driver.full_clean()
            driver.save()

            messages.success(request, 'Driver updated successfully!')
            return redirect('driver_detail', pk=driver.pk)

        except ValidationError as error:
            if hasattr(error, 'message_dict'):
                for field_errors in error.message_dict.values():
                    for error_message in field_errors:
                        messages.error(request, error_message)
            else:
                for error_message in error.messages:
                    messages.error(request, error_message)

    return render(
        request,
        'drivers/driver_update.html',
        {'driver': driver}
    )


def driver_delete(request, pk):

    driver = get_object_or_404(Driver, pk=pk)

    if request.method == 'POST':

        driver.delete()

        messages.success(request, 'Driver deleted successfully!')

        return redirect('driver_list')

    return render(
        request,
        'drivers/driver_delete.html',
        {'driver': driver}
    )