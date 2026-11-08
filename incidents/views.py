from django.shortcuts import render

# Create your views here.

from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Incident
from vehicles.models import Vehicle


class IncidentForm(forms.ModelForm):

    class Meta:
        model = Incident

        fields = [
            'vehicle',
            'title',
            'incident_type',
            'description',
            'location',
            'incident_date',
            'severity',
            'status',
            'estimated_damage',
            'evidence',
            'resolution_notes',
        ]

        widgets = {
            'vehicle': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter incident title'
            }),
            'incident_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: Accident, Breakdown'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter incident location'
            }),
            'incident_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'severity': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estimated_damage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'evidence': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'resolution_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

        input_formats = {
            'incident_date': ['%Y-%m-%dT%H:%M']
        }


@login_required
def incident_list(request):

    incidents = Incident.objects.select_related(
        'vehicle',
        'reported_by'
    ).order_by('-incident_date')

    search = request.GET.get('search', '').strip()

    if search:
        incidents = incidents.filter(
            title__icontains=search
        ) | incidents.filter(
            vehicle__vehicle_number__icontains=search
        )

    return render(
        request,
        'incidents/incident_list.html',
        {'incidents': incidents, 'search': search}
    )


@login_required
def incident_detail(request, pk):

    incident = get_object_or_404(Incident, pk=pk)

    return render(
        request,
        'incidents/incident_detail.html',
        {'incident': incident}
    )


@login_required
def incident_create(request):

    if request.method == 'POST':
        form = IncidentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()

            messages.success(
                request,
                'Incident reported successfully.'
            )

            return redirect('incident_list')

        messages.error(
            request,
            'Please correct the errors below.'
        )

    else:
        form = IncidentForm()

    return render(
        request,
        'incidents/incident_form.html',
        {'form': form, 'page_title': 'Report New Incident'}
    )


@login_required
def incident_update(request, pk):

    incident = get_object_or_404(Incident, pk=pk)

    if request.method == 'POST':
        form = IncidentForm(
            request.POST,
            request.FILES,
            instance=incident
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Incident updated successfully.'
            )

            return redirect('incident_detail', pk=incident.pk)

        messages.error(
            request,
            'Please correct the errors below.'
        )

    else:
        form = IncidentForm(instance=incident)

    return render(
        request,
        'incidents/incident_form.html',
        {
            'form': form,
            'page_title': 'Update Incident',
            'incident': incident
        }
    )


@login_required
def incident_delete(request, pk):

    incident = get_object_or_404(Incident, pk=pk)

    if request.method == 'POST':
        incident.delete()

        messages.success(
            request,
            'Incident deleted successfully.'
        )

        return redirect('incident_list')

    return render(
        request,
        'incidents/incident_confirm_delete.html',
        {'incident': incident}
    )
