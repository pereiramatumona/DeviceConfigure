
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.config_devices, name='config_devices' ),
    path('add_device', views.add_device, name='add_device' ),
    path('config_devices', views.config_devices, name='config_devices'),
    path('carregar_area', views.carregar_area, name='carregar_area' ),
    #Execução
    path('run_command', views.run_command, name='run_command' ),
    path('remove_element', views.remove_element, name='remove_element' ),
    path('writing_the_file', views.writing_the_file, name='writing_the_file'),
]