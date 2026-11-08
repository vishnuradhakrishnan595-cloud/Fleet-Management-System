
from django.urls import path
from . import views

urlpatterns = [
    path('', views.fuel_list, name='fuel_list'),
    path('create/', views.fuel_create, name='fuel_create'),
    path('<int:pk>/', views.fuel_detail, name='fuel_detail'),
    path('<int:pk>/edit/', views.fuel_update, name='fuel_update'),
]
