
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

from django.shortcuts import render

def home(request):
    return render(request, 'dashboard.html')


# --------------------------------------------------
# MAIN URL PATTERNS
# --------------------------------------------------

urlpatterns = [

    # Home
    path('', home, name='home'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Accounts and Authentication
    path('accounts/', include('accounts.urls')),

    # Vehicle Management
    path('vehicles/', include('vehicles.urls')),

    # Driver Management
    path('drivers/', include('drivers.urls')),

    # Trip Management
    path('trips/', include('trips.urls')),

    # Fuel Management
    path('fuel/', include('fuel.urls')),

    # Maintenance Management
    path('maintenance/', include('maintenance.urls')),

    # Expense Management
    path('expenses/', include('expenses.urls')),

    # Document Management
    path('documents/', include('documents.urls')),

    # Incident Management
    path('incidents/', include('incidents.urls')),

    # Notification Management
    path('notifications/', include('notifications.urls')),

    # Reports and Analytics
    path('reports/', include('reports.urls')),

]


# --------------------------------------------------
# MEDIA FILE CONFIGURATION
# --------------------------------------------------

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
