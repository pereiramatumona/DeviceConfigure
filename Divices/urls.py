
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.config_devices, name='config_devices' ),
    path('add_device', views.add_device, name='add_device' ),
    path('config_devices', views.config_devices, name='config_devices' ),
    path('carregar_area', views.carregar_area, name='carregar_area' ),
]