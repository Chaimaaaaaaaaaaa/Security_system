from gpiozero import MotionSensor
import datetime
import smtplib
from email.message import EmailMessage
import os
import time
import socket
import subprocess

# Fonction pour récupérer l'adresse IP locale sur le réseau
def get_ipv4_address():
    # Récupère l'adresse IP associée à l'interface réseau active (Wi-Fi, Ethernet)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # On utilise google.com comme serveur pour trouver l'IP
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        print(f"Erreur lors de la récupération de l'IP : {e}")
        ip_address = None
    finally:
        s.close()
    return ip_address


# Fonction pour envoyer un email avec le lien du flux vidéo
def send_email_gmail(subject, message, destination):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Remplacez par le mot de passe d'application
    server.login('braspeyy@gmail.com', 'mpsg ptgf sfvx wcys')

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = 'braspeyy@gmail.com'
    msg['To'] = destination

    server.send_message(msg)
    server.quit()

# Lire l'adresse e-mail à partir du fichier mail.txt écrit par le code usb.py
def read_email_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Email:"):
                return line.strip().split(":")[1].strip()  # On récupère l'email et on enlève les espaces autour
    return None

# Initialisation du capteur et de la caméra
pir = MotionSensor(15)

# Lire l'adresse email dans mail.txt
email_destination = read_email_from_file("/home/abc/Desktop/Projet_IOT/mail.txt")

if email_destination:
    print(f"Envoi des mail : {email_destination}")
else:
    print("Adresse e-mail non trouvée dans le fichier.")


while True:
    print("Détection de mouvement en cours...")
    pir.wait_for_motion()  # Attendre un mouvement
    print("Mouvement détecté")

    ip = get_ipv4_address() # Récupérer l'IP locale
    stream_url = f"http://{ip}:8000"  # Utilisation de l'IP locale
    print(f"URL de streaming : {stream_url}")  # Pour vérifier l'IP et l'URL

    if email_destination:
        send_email_gmail(
	    subject="Mouvement détecté - Flux en direct",
            message=f"Un mouvement a été détecté. Vous pouvez visualiser le flux en direct de la caméra à l'adresse suivante : {stream_url}",
            destination=email_destination
        )
            
        # Lancer le script server.py
        try:
            process = subprocess.Popen(['python3', '/home/abc/Desktop/Projet_IOT/stream.py'])  # Lance server.py en mode non-bloquant
            print("Le serveur a été lancé.")
            process.wait()
        except Exception as e:
            print(f"Erreur lors du lancement du serveur : {e}")
     
        # Attendre la fin du mouvement
        pir.wait_for_no_motion()
    else:
        print("Aucune adresse e-mail valide trouvée.")
