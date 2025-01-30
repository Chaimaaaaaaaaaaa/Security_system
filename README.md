# Surveillance à Distance avec Raspberry Pi

## Introduction
Ce projet permet de surveiller un lieu à distance en détectant un mouvement via un capteur PIR connecté à un Raspberry Pi. Lorsqu'un mouvement est détecté, un email est envoyé à l'utilisateur avec un lien permettant de visualiser en direct un flux vidéo de la caméra.

## Matériel Requis
- Raspberry Pi (4)
- Capteur PIR (HC-SR501 ou équivalent)
- Caméra compatible Raspberry Pi

## Fonctionnement
1. Le capteur PIR détecte un mouvement.
2. L'adresse IP locale est récupérée pour construire un lien de streaming.
3. Un email est envoyé à l'utilisateur contenant ce lien.
4. Un serveur HTTP démarre et diffuse le flux en direct.

## Schéma d'Architecture

![Capture d'écran 2025-01-30 085335](https://github.com/user-attachments/assets/f6c57d0f-2df1-4bdf-9a00-5d6777244d44)
Schéma software 

![Capture d'écran 2025-01-30 084859](https://github.com/user-attachments/assets/227eee4e-ef2e-4afe-90e0-122c5ce396d3)
Schéma hardware

## Installation & Configuration
### 1. Préparer le Raspberry Pi
- Installer Raspberry Pi OS.
- Activer la caméra avec la commande :
  ```bash
  sudo raspi-config
  ```
  Allez dans "Interface Options" > "Camera" > "Enable".
- Installer les dépendances nécessaires 

### 2. Scripts Python
#### **usb.py** (Lecture des identifiants Wi-Fi et email depuis une clé USB)
Ce script récupère l'email et les informations Wi-Fi à partir d'un fichier texte nommé `mon_fichier.txt` (format dans `config_usb/`) sur une clé USB et connecte le Raspberry Pi au réseau.

#### **final.py** (Détection de mouvement et envoi d'email)
Ce script surveille le capteur PIR, récupère l'adresse IP et envoie un email avec le lien du flux vidéo.
> **Note** : Pour ce projet, il faut créer une adresse email d'expédition et générer un *mot de passe d'application* via [Google App Passwords](https://myaccount.google.com/apppasswords).

Exemple de connexion SMTP :
```python
server.login('votre_email@gmail.com', 'mot_de_passe_application')
```

#### **stream.py** (Diffusion du flux caméra)
Ce script démarre un serveur HTTP qui diffuse le flux MJPEG en direct.
> **Note** : Pour visualiser le stream, il est nécessaire d'être connecté sur le même réseau Wi-Fi que le Raspberry Pi.
> **Basé sur** : Parikh, D. "How to Live Stream the Raspberry Pi Camera" - Raspberry Tips [(source)](https://raspberrytips.com/how-to-live-stream-pi-camera/)

### 3. Exécution automatique au démarrage
Pour exécuter `usb.py` et `final.py` au démarrage, ajoutez les lignes suivantes à la fin du fichier `.bashrc` :

```bash
nano ~/.bashrc
```

Ajoutez :
```bash
python3 /chemin/vers/usb.py 
python3 /chemin/vers/final.py 
```

## Exécution
1. Branchez la clé USB contenant les identifiants Wi-Fi.
2. `usb.py` et `final.py` sont exécutés au démarrage du Raspberry Pi.
3. `usb.py` se charge de la connexion au Wi-Fi et crée un fichier `mail.txt` contenant l'adresse email indiquée sur la clé USB.
4. À la fin de l'exécution de `usb.py`, `final.py` est automatiquement lancé.
5. Lorsqu'un mouvement est détecté, `final.py` lance `stream.py` pour la diffusion en direct.
6. Pour reprendre la détection de mouvement, assurez-vous d'arrêter `stream.py` en cliquant sur "Stop Stream" sur la page HTML avant de retourner à `final.py`.

## Améliorations Possibles
- Ajouter une IA pour détecter les visages et éviter les fausses alertes.
- Stocker les vidéos en cas d'intrusion.
- Accès au flux vidéo depuis un réseau externe (via un tunnel SSH ou une solution cloud).
- Ajouter un servomoteur pour contrôler l'angle de la caméra.

## Conclusion
Ce projet fournit une solution efficace et économique pour surveiller un lieu à distance. Grâce à un Raspberry Pi et quelques composants, il est possible d’avoir un système de détection et de streaming vidéo accessible depuis un simple email.
