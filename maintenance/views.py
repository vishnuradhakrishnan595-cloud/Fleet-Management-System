
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Maintenance
from vehicles.models import Vehicle


class MaintenanceForm(forms.ModelForm):

    class Meta:
        model = Maintenance

        fields = [
            'vehicle',
            'maintenance_type',
            'title',
            'description',
            'service_date',
            'next_service_date',
            'odometer_reading',
            'service_center',
            'cost',
            'status',
        ]

        widgets = {
            'vehicle': forms.Select(attrs={
                'class': 'form-select'
            }),
            'maintenance_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter maintenance title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the maintenance work'
            }),
            'service_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'next_service_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'odometer_reading': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'service_center': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service center'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        service_date = cleaned_data.get('service_date')
        next_service_date = cleaned_data.get('next_service_date')
        cost = cleaned_data.get('cost')
        odometer = cleaned_data.get('odometer_reading')

        if service_date and next_service_date:
            if next_service_date < service_date:
                self.add_error(
                    'next_service_date',
                    'Next service date cannot be before the service date.'
                )

        if cost is not None and cost < 0:
            self.add_error('cost', 'Cost cannot be negative.')

        if odometer is not None and odometer < 0:
            self.add_error(
                'odometer_reading',
                'Odometer reading cannot be negative.'
            )

        return cleaned_data


@login_required
def maintenance_list(request):

    records = Maintenance.objects.select_related(
        'vehicle',
        'performed_by'
    ).order_by('-service_date')

    search = request.GET.get('search', '').strip()

    if search:
        records = records.filter(
            Q(title__icontains=search) |
            Q(vehicle__vehicle_number__icontains=search) |
            Q(service_center__icontains=search) |
            Q(maintenance_type__icontains=search)
        )

    return render(
        request,
        'maintenance/maintenance_list.html',
        {
            'records': records,
            'search': search,
        }
    )


@login_required
def maintenance_detail(request, pk):

    record = get_object_or_404(
        Maintenance.objects.select_related('vehicle', 'performed_by'),
        pk=pk
    )

    return render(
        request,
        'maintenance/maintenance_detail.html',
        {'record': record}
    )


@login_required
def maintenance_create(request):

    if request.method == 'POST':
        form = MaintenanceForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.performed_by = request.user
            record.save()

            messages.success(
                request,
                'Maintenance record created successfully.'
            )

            return redirect('maintenance_list')

        messages.error(request, 'Please correct the errors below.')

    else:
        form = MaintenanceForm()

    return render(
        request,
        'maintenance/maintenance_form.html',
        {
            'form': form,
            'page_title': 'Add Maintenance Record',
        }
    )


@login_required
def maintenance_update(request, pk):

    record = get_object_or_404(Maintenance, pk=pk)

    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=record)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Maintenance record updated successfully.'
            )

            return redirect('maintenance_detail', pk=record.pk)

        messages.error(request, 'Please correct the errors below.')

    else:
        form = MaintenanceForm(instance=record)

    return render(
        request,
        'maintenance/maintenance_form.html',
        {
            'form': form,
            'page_title': 'Update Maintenance Record',
            'record': record,
        }
    )


@login_required
def maintenance_delete(request, pk):

    record = get_object_or_404(Maintenance, pk=pk)

    if request.method == 'POST':
        record.delete()

        messages.success(
            request,
            'Maintenance record deleted successfully.'
        )

        return redirect('maintenance_list')

    return render(
        request,
        'maintenance/maintenance_confirm_delete.html',
        {'record': record}
    )
