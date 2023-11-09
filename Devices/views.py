from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from .models import Devices

#netmiko
from netmiko import ConnectHandler
from getpass import getpass
from netmiko import ConnectHandler
#from netmiko.ssh_exception import SSHException

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
    
    if request.method == 'GET':
        devices = Devices.objects.all()

        context = {
            'devices':devices
            }

        tobe_configured = {
            'device':read_file()
        }

        return render(request, 'config_devices.html', {'context':context,'tobe_configured':tobe_configured})
    else:
      
        return render(request, 'config_devices.html', {})
    

def carregar_area(request):
    devices = Devices.objects.all()

    context = {
        'devices':devices
        }
    
    config_devices = request.POST.get('config_area')

    print(f'AREA: {config_devices}')

    return render(request, 'config_devices.html', {'context':context,})




def run_command(request):
    if request.method == 'GET':
        return render(request, 'config_devices.html' )  
      
    if request.method == 'POST':
        command_area = request.POST.get('command_area')
        if len(command_area.strip()) == 0:
            messages.add_message(request,constants.ERROR, 'Insert the commands on command fields...')
            return redirect('config_devices')
        else:
            #print( command_area)
            lounch_command(read_file(), command_validation(command_area) )
            #print( command_validation(command_area))



            
            return redirect('config_devices') 
        


def command_validation(command):
    
    command_validated = command.split('\r\n')

    return command_validated

def read_file():
    obj_compiled = []

    with open('device_conf.dat', 'r+' ) as device_file:
        for device in device_file:
            componentes = device.split(';')
            obj_compiled.append(componentes)

    #print(obj_compiled)
        
    return obj_compiled 


def remove_element(request):
    
    obj_rem = []
    obj_list = dict(request.POST)

    if request.method == 'POST':

        for removed_device in obj_list:
            if removed_device != 'csrfmiddlewaretoken':    
                #print(removed_device)
                #remove_from_file(removed_device)
                obj_rem.append(removed_device)
        #print(obj_rem)
        remove_from_file(obj_rem)
        
    return redirect('config_devices')


def remove_from_file(element):
    obj_compiled = []

    with open('device_conf.dat', 'r+' ) as device_file:
        for device in device_file:
            componentes = device.split(';')

            #print(componentes[1])
            if not componentes[1] in element:
                #print('DEV', componentes)
                obj_compiled.append(componentes)

    with open('device_conf.dat', 'w' ) as device_file_:
        for device_to_write in obj_compiled:
            if device_to_write in obj_compiled:
                device_file_.write(';'.join(device_to_write))
        device_file_.write('\n')
            

            #obj_compiled.append(componentes)


def writing_the_file(request):
    if request.method == 'POST':
        for device in request.POST:
            if device != 'csrfmiddlewaretoken':
                print(device)
                with open('device_conf.dat', 'a+') as device_file:
                    device_file.write(device+';not yet')
        #device_file.write('\n')
    return redirect('/config_devices')


def lounch_command(device_list, command_list):
    #device_obj = {
    #    "device_type": "cisco_ios",
    #    "host": "cisco1.lasthop.io",
    #    "username": "pyclass",
    #    "password": password,
    #    }
    device_obj = {}
    device_list_updated = []
    #password = getpass()

    for device in device_list:
        #print('DEVICE: ', device[1])
        device_obj['device_type'] = 'cisco_ios'
        device_obj['host'] = device[1]
        device_obj['username'] = 'username'
        device_obj['password'] = 'password'
        device_list_updated.append(device_obj)

    for devices_objected in device_list_updated:
        try:
            net_connect = ConnectHandler(**devices_objected)
            output = net_connect.send_config_set(command_list)
            print(f'{devices_objected['host']} - {output} ')

        except Exception as err:
            print('Timeout', err)
            continue
            
