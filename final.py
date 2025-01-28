from gpiozero import MotionSensor
from picamzero import Camera
import datetime
import smtplib
from email.message import EmailMessage
import os
import time

# Fonction pour envoyer un email avec une photo ou vidéo en pièce jointe
def send_email_gmail(subject, message, destination, media_path, media_type='image'):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Remplacez par votre mot de passe d'application
    server.login('braspeyy@gmail.com', 'mpsg ptgf sfvx wcys')

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = 'braspeyy@gmail.com'
    msg['To'] = destination

    # Ajouter la photo/vidéo en pièce jointe
    with open(media_path, 'rb') as media:
        file_data = media.read()
        file_name = os.path.basename(media_path)
        if media_type == 'image':
            msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)
        else:
            msg.add_attachment(file_data, maintype='video', subtype='mp4', filename=file_name)

    server.send_message(msg)
    server.quit()

# Lire l'adresse e-mail à partir du fichier mail.txt
def read_email_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Email:"):
                return line.strip().split(":")[1].strip()  # On récupère l'email et on enlève les espaces autour
    return None

# Initialisation du capteur et de la caméra
pir = MotionSensor(15)
camera = Camera()


# Lire l'adresse email dans mail.txt
email_destination = read_email_from_file("mail.txt")

if email_destination:
    print(f"Envoi des photos à : {email_destination}")
else:
    print("Adresse e-mail non trouvée dans le fichier.")

# Fonction pour attendre sans rien faire pendant un certain temps
def wait_for_next_detection(timeout):
    print(f"En attente de {timeout / 60} minutes avant de détecter à nouveau...")
    time.sleep(timeout)

# Compteur pour alterner entre photo et vidéo
motion_count = 0


while True:
    print("Détection de mouvement en cours...")
    pir.wait_for_motion()  # Attendre un mouvement
    print("Mouvement détecté")

    motion_count += 1

    # Capture de la photo 
    photo_path = f"/home/abc/Desktop/Projet_IOT/img/photo.jpg"

    if motion_count == 1:  # Premier et tous les mouvements impairs => photo
        print("Prise de photo...")
        camera.take_photo(photo_path)

        if email_destination:
            # Envoi du mail avec la photo en pièce jointe
            send_email_gmail(
                subject="Mouvement détecté - Photo", 
                message="Un mouvement a été détecté, voici la photo prise.", 
                destination=email_destination, 
                media_path=photo_path, 
                media_type='image'
            )
            
            # Attendre la fin du mouvement
            pir.wait_for_no_motion()
        else:
            print("Aucune adresse e-mail valide trouvée.")

    else:  # Tous les mouvements pairs => vidéo
        print("Enregistrement vidéo de 1 minute...")
        video_path = f"/home/abc/Desktop/Projet_IOT/img/video.mp4"
        camera.record_video(video_path, duration=60)  # Enregistrer une vidéo de 1 minute

        if email_destination:
            # Envoi du mail avec la vidéo en pièce jointe
            send_email_gmail(
                subject="Mouvement détecté - Vidéo", 
                message="Un mouvement a été détecté, voici la vidéo enregistrée.", 
                destination=email_destination, 
                media_path=video_path, 
                media_type='video'
            )
            # Attendre la fin du mouvement
            pir.wait_for_no_motion()
        else:
            print("Aucune adresse e-mail valide trouvée.")
            
        # Attendre 10 minutes avant de traiter une nouvelle détection
        motion_count = 0
        wait_for_next_detection(600)  # 600 secondes = 10 minutes
   


