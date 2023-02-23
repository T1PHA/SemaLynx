from django.shortcuts import render
import paramiko
import socket
from django.http import HttpResponse
from django.shortcuts import render
import os
import ping3
import re


def index(request):
    return render(request, "main.html")

def main(request):
    machines = [
        {'name': 'Semabox 1', 'ip': '192.168.146.138'},
        {'name': 'Semabox 2', 'ip': '192.168.146.128'},
        {'name': 'Semabox 3', 'ip': '192.168.146.1'},
    ]

    for machine in machines:
        machine['Etat'] = 'En ligne' if ping3.ping(machine['ip']) else 'Hors ligne'

    # if request.method == 'POST':
    #     # Get the machine index from the form
    #     index = int(request.POST['machine'])
    #     # Get the machine object from the machines list
    #     machine = machines[index]
    #     # Create a SSH client
    #     client = paramiko.SSHClient()
    #     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     # Connect to the machine
    #     client.connect(machine['ip'], username='kali', password='kali')
    #     # Send the reboot command
    #     stdin, stdout, stderr = client.exec_command('sudo reboot')
    #     # Close the connection
    #     client.close()

    context = {'machines': machines}
    return render(request, 'main.html', context)

##############RESTART##########################
def simple_function(request):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.146.138", username='kali', password='kali')

    stdin, stdout, stderr = client.exec_command("sudo reboot") #nmap -sV 172.16.234.100
    for line in stdout.read().splitlines():
        print (line)
        

    client.close()


    print("Session fermée")
    return HttpResponse("""<html><script>window.location.replace('/');<script><html>""")

def simple_function2(request):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.146.128", username='kali', password='kali')

    stdin, stdout, stderr = client.exec_command("sudo reboot") #nmap -sV 172.16.234.100
    for line in stdout.read().splitlines():
        print (line)
        

    client.close()


    print("Session fermée")
    return render(request, 'main.html')

def simple_function3(request):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.146.1", username='kali', password='kali')

    stdin, stdout, stderr = client.exec_command("sudo reboot") #nmap -sV 172.16.234.100
    for line in stdout.read().splitlines():
        print (line)
        

    client.close()


    print("Session fermée")
    return render("""<html><script>window.location.replace('/');<script><html>""")
    
#####################TDB#######################

def machine_info(request):

    # établir une connexion SSH avec la machine distante
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="192.168.146.138", username="kali", password="kali")

    # exécuter une commande pour tester le fonctionnement de la connexion Internet
    stdin, stdout, stderr = ssh_client.exec_command('ping -c 1 google.com')
    test_ping = stdout.read().decode().strip()
    
    # exécuter une commande pour tester le débit de la connexion Internet
    # METTRE IP DE SEMALYNX
    stdin, stdout, stderr = ssh_client.exec_command("iperf3 -c 192.168.146.134 -i 1 -t 1")
    output = stdout.read().decode('utf-8')
    test_debit= re.findall(r"(\d+\.\d+)\s*MBytes", output)

    # exécuter une commande pour obtenir l'adresse IP de la machine distante
    stdin, stdout, stderr = ssh_client.exec_command('hostname -I')
    machine_ip = stdout.read().decode().strip()
    
    #nom de la machine
    stdin, stdout, stderr = ssh_client.exec_command('hostname')
    machine_nom = stdout.read().decode().strip()
    
    # Exécution de la commande pour récupérer les adresses IP des machines connectées au réseau local
    stdin, stdout, stderr = ssh_client.exec_command("arp -a | awk '{print $2}' | cut -d '(' -f2 | cut -d ')' -f1")
    ip_list = stdout.read().decode().strip()

    # fermer la connexion SSH
    ssh_client.close()

    # préparer les données pour le rendu de la page
    context = {
        'ip_address': machine_ip,
        'test_ping': test_ping,
        'test_debit': test_debit,
        'nom': machine_nom,
        'ip_list': ip_list,
    }
    
    if "1 received" in test_ping:
            context['connected'] = True
    else:
            context['connected'] = False


    # rendre la page HTML avec les résultats
    return render(request, 'machine_info.html', context=context)


def machine_info2(request):

    # établir une connexion SSH avec la machine distante
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="192.168.146.128", username="kali", password="kali")

    # exécuter une commande pour tester le fonctionnement de la connexion Internet
    stdin, stdout, stderr = ssh_client.exec_command('ping -c 1 google.com')
    test_ping = stdout.read().decode().strip()
    
    # exécuter une commande pour tester le débit de la connexion Internet
    # METTRE IP DE SEMALYNX
    stdin, stdout, stderr = ssh_client.exec_command("iperf3 -c 192.168.146.134 -i 1 -t 1")
    output = stdout.read().decode('utf-8')
    test_debit= re.findall(r"(\d+\.\d+)\s*MBytes", output)

    # exécuter une commande pour obtenir l'adresse IP de la machine distante
    stdin, stdout, stderr = ssh_client.exec_command('hostname -I')
    machine_ip = stdout.read().decode().strip()
    
    #nom de la machine
    stdin, stdout, stderr = ssh_client.exec_command('hostname')
    machine_nom = stdout.read().decode().strip()
    
    # Exécution de la commande pour récupérer les adresses IP des machines connectées au réseau local
    stdin, stdout, stderr = ssh_client.exec_command("arp -a | awk '{print $2}' | cut -d '(' -f2 | cut -d ')' -f1")
    ip_list = stdout.read().decode().strip()

    # fermer la connexion SSH
    ssh_client.close()

    # préparer les données pour le rendu de la page
    context = {
        'ip_address': machine_ip,
        'test_ping': test_ping,
        'test_debit': test_debit,
        'nom': machine_nom,
        'ip_list': ip_list,
    }
    
    if "1 received" in test_ping:
            context['connected'] = True
    else:
            context['connected'] = False


    # rendre la page HTML avec les résultats
    return render(request, 'machine_info.html', context=context)
    
    
def machine_info3(request):

    # établir une connexion SSH avec la machine distante
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="192.168.146.1", username="tiph", password="197207")

    # exécuter une commande pour tester le fonctionnement de la connexion Internet
    stdin, stdout, stderr = ssh_client.exec_command('ping -c 1 google.com')
    test_ping = stdout.read().decode().strip()
    
    # exécuter une commande pour tester le débit de la connexion Internet
    # METTRE IP DE SEMALYNX
    stdin, stdout, stderr = ssh_client.exec_command("iperf3 -c 192.168.146.134 -i 1 -t 1")
    output = stdout.read().decode('utf-8')
    test_debit= re.findall(r"(\d+\.\d+)\s*MBytes", output)

    # exécuter une commande pour obtenir l'adresse IP de la machine distante
    stdin, stdout, stderr = ssh_client.exec_command('hostname -I')
    machine_ip = stdout.read().decode().strip()
    
    #nom de la machine
    stdin, stdout, stderr = ssh_client.exec_command('hostname')
    machine_nom = stdout.read().decode().strip()
    
    # Exécution de la commande pour récupérer les adresses IP des machines connectées au réseau local
    stdin, stdout, stderr = ssh_client.exec_command("arp -a | awk '{print $2}' | cut -d '(' -f2 | cut -d ')' -f1")
    ip_list = stdout.read().decode().strip()

    # fermer la connexion SSH
    ssh_client.close()

    # préparer les données pour le rendu de la page
    context = {
        'ip_address': machine_ip,
        'test_ping': test_ping,
        'test_debit': test_debit,
        'nom': machine_nom,
        'ip_list': ip_list,
    }
    
    if "1 received" in test_ping:
            context['connected'] = True
    else:
            context['connected'] = False


    # rendre la page HTML avec les résultats
    return render(request, 'machine_info.html', context=context)
