from django.shortcuts import render, HttpResponse
from .models import Devices

# Create your views here.


def add_device(request):

    fabricantes = Devices.fabricante_choices
    devices = Devices.objects.all()

    context = {
        'fabricantes': fabricantes,
        'devices':devices
    }

    return render(request, 'add_device.html', {'context':context})

    

def config_devices(request):
    
    devices = Devices.objects.all()

    context = {
        'devices':devices
        }

    return render(request, 'config_devices.html', {'context':context,})

