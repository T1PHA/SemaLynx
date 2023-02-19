from django.shortcuts import render
import paramiko
import socket
from django.http import HttpResponse
from django.shortcuts import render
import os
import ping3


def index(request):
    return render(request, "main.html")

def main(request):
    machines = [
        {'name': 'Semabox 1', 'ip': '193.168.1.128'},
        {'name': 'Semabox 2', 'ip': '192.168.1.101'},
        {'name': 'Semabox 3', 'ip': '192.168.1.102'},
    ]

    for machine in machines:
        machine['status'] = 'Online' if ping3.ping(machine['ip']) else 'Offline'

    if request.method == 'POST':
        # Get the machine index from the form
        index = int(request.POST['machine'])
        # Get the machine object from the machines list
        machine = machines[index]
        # Create a SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the machine
        client.connect(machine['ip'], username='kali', password='kali')
        # Send the reboot command
        stdin, stdout, stderr = client.exec_command('sudo reboot')
        # Close the connection
        client.close()

    context = {'machines': machines}
    return render(request, 'main.html', context)

# def machine_status(request):
#     machines = ['193.168.1.128', '192.168.1.101', '192.168.1.102']
#     statuses = {}
#     for machine in machines:
#         response = os.system("ping" + machine)
#         if response == 0:
#             statuses[machine] = 1
#         else:
#             statuses[machine] = 0
#     return render(request, 'main.html', {'machines': machines, 'statuses': statuses})

# def machine_restart(request, machine_ip):
#     response = os.system("ping -c 1 " + machine_ip)
#     if response == 0:
#         os.system("ssh root@" + machine_ip + " 'reboot'")
#         message = machine_ip + " is being restarted"
#     else:
#         message = machine_ip + " is offline"
#     return render(request, 'main.html', {'message': message})

# def scan_network():
#     hostname = socket.gethostbyname(socket.gethostname())
#     ip_range = '.'.join(hostname.split('.')[0:-1]) + '.'
#     for i in range(1, 255):
#         address = ip_range + str(i)
#         try:
#             host = socket.gethostbyaddr(address)
#             print(host[0], 'is up')
#         except:
#             print(address, 'is down')

# def machines_list(request):
    # # Connexion SSH avec Paramiko
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('193.168.1.128', username='kali', password='kali')

    # # Récupération de la liste des machines présentes dans le réseau
    # stdin, stdout, stderr = ssh.exec_command('ls')
    # machines = stdout.read().decode('utf-8').split('\n')

    # # Fermeture de la connexion SSH
    # ssh.close()

#     # # Rendu de la vue avec la liste des machines
#     # return render(request, 'machines_list.html', {'machines': machines})