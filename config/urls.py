
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>Fleet Management System</h1>"
        "<p>Welcome!</p>"
    )


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # Vehicles
    path('vehicles/', include('vehicles.urls')),

    # Drivers
    path('drivers/', include('drivers.urls')),

    # Documents
    path('documents/', include('documents.urls')),

    # Expenses
    path('expenses/', include('expenses.urls')),

    # Fuel
    path('fuel/', include('fuel.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
