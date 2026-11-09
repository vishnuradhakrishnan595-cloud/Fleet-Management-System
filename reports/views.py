from django.shortcuts import render

# Create your views here.

from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render
from django.utils import timezone

from vehicles.models import Vehicle
from fuel.models import FuelRecord
from maintenance.models import Maintenance
from expenses.models import Expense


def get_date_filters(request):
    """
    Read optional start_date and end_date from GET parameters.
    Invalid dates are ignored.
    """
    start_date = None
    end_date = None

    try:
        value = request.GET.get('start_date', '')
        if value:
            start_date = date.fromisoformat(value)
    except (ValueError, TypeError):
        pass

    try:
        value = request.GET.get('end_date', '')
        if value:
            end_date = date.fromisoformat(value)
    except (ValueError, TypeError):
        pass

    if start_date and end_date and start_date > end_date:
        start_date, end_date = end_date, start_date

    return start_date, end_date


def apply_date_filter(queryset, field_name, start_date, end_date):
    if start_date:
        queryset = queryset.filter(**{
            f'{field_name}__gte': start_date
        })

    if end_date:
        queryset = queryset.filter(**{
            f'{field_name}__lte': end_date
        })

    return queryset


def date_context(start_date, end_date):
    return {
        'start_date': start_date.isoformat() if start_date else '',
        'end_date': end_date.isoformat() if end_date else '',
    }


@login_required
def report_dashboard(request):

    start_date, end_date = get_date_filters(request)

    fuel_records = apply_date_filter(
        FuelRecord.objects.all(),
        'fuel_date',
        start_date,
        end_date
    )

    maintenance_records = apply_date_filter(
        Maintenance.objects.all(),
        'service_date',
        start_date,
        end_date
    )

    expense_records = apply_date_filter(
        Expense.objects.all(),
        'expense_date',
        start_date,
        end_date
    )

    total_vehicles = Vehicle.objects.count()

    total_fuel_cost = (
        fuel_records.aggregate(total=Sum('total_cost'))['total'] or 0
    )

    total_fuel_quantity = (
        fuel_records.aggregate(total=Sum('quantity'))['total'] or 0
    )

    total_maintenance_cost = (
        maintenance_records.aggregate(total=Sum('cost'))['total'] or 0
    )

    total_expenses = (
        expense_records.aggregate(total=Sum('amount'))['total'] or 0
    )

    context = {
        'total_vehicles': total_vehicles,
        'total_fuel_cost': total_fuel_cost,
        'total_fuel_quantity': total_fuel_quantity,
        'total_maintenance_cost': total_maintenance_cost,
        'total_expenses': total_expenses,
        'fuel_count': fuel_records.count(),
        'maintenance_count': maintenance_records.count(),
        'expense_count': expense_records.count(),
        'total_operational_cost': (
            total_fuel_cost +
            total_maintenance_cost +
            total_expenses
        ),
        **date_context(start_date, end_date),
    }

    return render(
        request,
        'reports/report_dashboard.html',
        context
    )


@login_required
def vehicle_report(request):

    vehicles = Vehicle.objects.all().order_by('vehicle_number')

    vehicle_summary = vehicles.values(
        'status'
    ).annotate(
        total=Count('id')
    ).order_by('status')

    context = {
        'vehicles': vehicles,
        'total_vehicles': vehicles.count(),
        'vehicle_summary': vehicle_summary,
    }

    return render(
        request,
        'reports/vehicle_report.html',
        context
    )


@login_required
def fuel_report(request):

    start_date, end_date = get_date_filters(request)

    records = FuelRecord.objects.select_related(
        'vehicle',
        'driver'
    ).order_by('-fuel_date')

    records = apply_date_filter(
        records,
        'fuel_date',
        start_date,
        end_date
    )

    summary = records.aggregate(
        total_quantity=Sum('quantity'),
        total_cost=Sum('total_cost'),
        total_records=Count('id')
    )

    vehicle_summary = records.values(
        'vehicle__vehicle_number'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_cost=Sum('total_cost'),
        total_records=Count('id')
    ).order_by('-total_cost')

    context = {
        'records': records,
        'total_quantity': summary['total_quantity'] or 0,
        'total_cost': summary['total_cost'] or 0,
        'total_records': summary['total_records'] or 0,
        'vehicle_summary': vehicle_summary,
        **date_context(start_date, end_date),
    }

    return render(
        request,
        'reports/fuel_report.html',
        context
    )


@login_required
def maintenance_report(request):

    start_date, end_date = get_date_filters(request)

    records = Maintenance.objects.select_related(
        'vehicle',
        'performed_by'
    ).order_by('-service_date')

    records = apply_date_filter(
        records,
        'service_date',
        start_date,
        end_date
    )

    summary = records.aggregate(
        total_cost=Sum('cost'),
        total_records=Count('id')
    )

    status_summary = records.values(
        'status'
    ).annotate(
        total=Count('id')
    ).order_by('status')

    context = {
        'records': records,
        'total_cost': summary['total_cost'] or 0,
        'total_records': summary['total_records'] or 0,
        'status_summary': status_summary,
        **date_context(start_date, end_date),
    }

    return render(
        request,
        'reports/maintenance_report.html',
        context
    )


@login_required
def expense_report(request):

    start_date, end_date = get_date_filters(request)

    records = Expense.objects.select_related(
        'vehicle',
        'recorded_by'
    ).order_by('-expense_date')

    records = apply_date_filter(
        records,
        'expense_date',
        start_date,
        end_date
    )

    summary = records.aggregate(
        total_amount=Sum('amount'),
        total_records=Count('id')
    )

    category_summary = records.values(
        'category'
    ).annotate(
        total_amount=Sum('amount'),
        total_records=Count('id')
    ).order_by('-total_amount')

    context = {
        'records': records,
        'total_amount': summary['total_amount'] or 0,
        'total_records': summary['total_records'] or 0,
        'category_summary': category_summary,
        **date_context(start_date, end_date),
    }

    return render(
        request,
        'reports/expense_report.html',
        context
    )
