
from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.report_dashboard,
        name='report_dashboard'
    ),

    path(
        'vehicles/',
        views.vehicle_report,
        name='vehicle_report'
    ),

    path(
        'fuel/',
        views.fuel_report,
        name='fuel_report'
    ),

    path(
        'maintenance/',
        views.maintenance_report,
        name='maintenance_report'
    ),

    path(
        'expenses/',
        views.expense_report,
        name='expense_report'
    ),

    path(
        'trips/',
        views.trip_report,
        name='trip_report'
    ),
]
