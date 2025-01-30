import os
import time
import subprocess

import sys

# Fonction pour détecter les périphériques USB montés
def detect_usb():
    mounted_devices = []
    for device in os.listdir('/media/abc'):
        mounted_devices.append(f"/media/abc/{device}")
    return mounted_devices

# Fonction pour lire un fichier et extraire les informations
def parse_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Contenu brut du fichier {file_path} :\n{content}")

            # Analyse le contenu pour extraire SSID, MDP et MAIL
            data = {}
            for line in content.splitlines():
                if line.startswith("SSID:"):
                    data['SSID'] = line.split(":", 1)[1].strip()
                elif line.startswith("MDP:"):
                    data['MDP'] = line.split(":", 1)[1].strip()
                elif line.startswith("MAIL:"):
                    data['MAIL'] = line.split(":", 1)[1].strip()
           
            print(f"Données extraites : {data}")
            return data
    except Exception as e:
        print(f"Erreur lors de la lecture ou de l'analyse du fichier {file_path} : {e}")
        return None
        
def write_email_to_file(email):
    try:
        # Nouveau chemin pour enregistrer le fichier
        file_path = '/home/abc/Desktop/Projet_IOT/mail.txt'
        
        # Écriture de l'email dans le fichier mail.txt
        with open(file_path, 'w') as file:
            file.write(f"Email: {email}\n")
            print(f"L'email a été écrit dans le fichier {file_path} : {email}")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier {file_path} : {e}")



def connect_wifi(ssid, password):
    # Commande pour se connecter au Wi-Fi
    print(f"Tentative de connexion au Wi-Fi {ssid}...")
    subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password])

    # Boucle pour vérifier si la connexion a réussi
    connected = False
    while not connected:
        # Vérifie l'état de la connexion
        result = subprocess.run(['nmcli', '-t', 'connection', 'show', '--active'], stdout=subprocess.PIPE)
        active_connections = result.stdout.decode().strip()
        
        if ssid in active_connections:
            print(f"Connecté au Wi-Fi {ssid} avec succès!")
            connected = True
        else:
            print(f"Échec de la connexion au Wi-Fi {ssid}, nouvelle tentative dans 5 secondes...")
            time.sleep(5)
            subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password])


# Dossier où les périphériques USB sont montés automatiquement
usb_mount_path = '/media/abc'

print("En attente de connexion USB...")

# Liste initiale des périphériques montés
initial_devices = detect_usb()

while True:

    # Vérifie périodiquement les périphériques montés
    time.sleep(2)
    current_devices = detect_usb()

    # Détecte un nouveau périphérique USB
    new_devices = list(set(current_devices) - set(initial_devices))
    if new_devices:
        for device in new_devices:
            print(f"Nouveau périphérique détecté : {device}")
             
            # Exemple : lire un fichier spécifique dans le périphérique USB
            file_path = os.path.join(device, 'mon_fichier.txt')
            if os.path.exists(file_path):
                data = parse_file(file_path)
                if data:
                    ssid = data.get('SSID', '')
                    mdp = data.get('MDP', '')
                    mail = data.get('MAIL', '')
                       
                    # Stocke les valeurs extraites
                    print(f"SSID: {ssid}")
                    print(f"MDP: {mdp}")
                    print(f"MAIL: {mail}")
                        
                    # Écrire l'email dans un fichier
                    write_email_to_file(mail)
                        
                    # Test avec des identifiants récupérés
                    connect_wifi(ssid, mdp)
                    sys.exit(0)

            else:
                print(f"Le fichier {file_path} n'existe pas sur le périphérique {device}")
            break
    # Met à jour la liste des périphériques montés
    initial_devices = current_devices
