from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from .models import Devices

# Create your views here.


def add_device(request):

    if request.method == 'GET':
        fabricantes = Devices.fabricante_choices
        devices = Devices.objects.all()
        context = {
            'fabricantes': fabricantes,
            'devices':devices
        }
        return render(request, 'add_device.html', {'context':context})
    else:
        device = request.POST.get('device')
        ip_addr = request.POST.get('ip_addr')
        fabricante = request.POST.get('manufacturing')

        if len(device.strip()) == 0 or len(ip_addr.strip()) == 0 or len(fabricante.strip()) == 0:

            messages.add_message(request,constants.ERROR,'Preencha todos os campos obrigatorios...')
            print(f'Name: {device}, \nIP ADDRESS: {ip_addr}, \nManufacturing: {fabricante}')
            return redirect('/add_device')
        else:
            device_carregado = Devices(
                device = device,
                ip_addr = ip_addr,
                fabricante = fabricante
            )

            device_carregado.save()

            messages.add_message(request,constants.SUCCESS,'Device save successfully...')
            print(f'Name: {device}, \nIP ADDRESS: {ip_addr}, \nManufacturing: {fabricante}')
            return redirect('/add_device')

def config_devices(request):
    
    devices = Devices.objects.all()

    context = {
        'devices':devices
        }

    return render(request, 'config_devices.html', {'context':context,})

