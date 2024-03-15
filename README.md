# Projet de suivi de cible avec caméra PTZ et détection d'objet

Ce projet vise à créer un système de suivi de cible en utilisant une caméra Pan-Tilt-Zoom (PTZ) contrôlée via ONVIF et une détection d'objet en temps réel à l'aide du modèle YOLO (You Only Look Once). Le système est conçu pour suivre une cible spécifique dans un flux vidéo, contrôler la caméra pour garder la cible au centre de l'image, et effectuer des actions de zoom en fonction de la taille de la cible.

## Fonctionnalités principales

- **Détection d'objet YOLO** : Utilise le modèle YOLO pour détecter et suivre une cible spécifique dans le flux vidéo en temps réel.
- **Contrôle PTZ via ONVIF** : Contrôle la caméra PTZ via le protocole ONVIF pour maintenir la cible au centre de l'image.
- **Suivi de cible précis** : Effectue des mouvements de la caméra en fonction de la position de la cible détectée pour la maintenir au centre de l'image.
- **Actions de zoom automatiques** : Effectue des actions de zoom avant/arrière en fonction de la taille de la cible par rapport à une référence.
- **Capture d'image** : Permet de capturer des images à partir du flux vidéo lorsque la cible est détectée et lorsqu'elle est centrée.

## Contenu du projet

Le projet est structuré en plusieurs fichiers Python:

- **Main.py** : Le fichier principal qui orchestre le fonctionnement du système, il charge la configuration à partir d'un fichier JSON, initialise les composants, contrôle la caméra et déclenche la détection d'objet.
  
- **Controle_ONVIF.py** : Fournit une classe `OnvifPTZCamera` pour contrôler la caméra PTZ via ONVIF, y compris les mouvements de panoramique, d'inclinaison et de zoom, ainsi que la fonction de calibration.

- **DetectBird.py** : Contient la logique de détection et de suivi de la cible dans le flux vidéo à l'aide du modèle YOLO. Il capture également des images lorsqu'une cible est détectée et lorsqu'elle est centrée.

- **Test_ONVIF.py** : Un script de test qui permet de visualiser le flux vidéo en utilisant OpenCV et de contrôler la caméra PTZ pour observer son comportement en temps réel.

- **Export_PT_to_Engine.py** : Script utilisé pour exporter le modèle YOLO dans un format engine qui est plus rapide.

Le projet contient également un fichier `Config.json` qui stocke la configuration du système, ainsi qu'un script `dependencies.bash` pour installer les dépendances Python nécessaires.

## Installation des dépendances

Exécutez le script `dependencies.bash` pour installer les dépendances Python requises pour le projet. Assurez-vous d'avoir Python 3 installé sur votre système.

```bash
./dependencies.bash
```

## Utilisation

1. Assurez-vous d'avoir une caméra PTZ compatible ONVIF connectée au réseau et correctement configurée.

2. Modifiez le fichier `Config.json` avec les détails de votre configuration, y compris les adresses IP, les ports, les identifiants de connexion et d'autres paramètres pertinents.

3. Exécutez le fichier `Main.py` pour démarrer le système de suivi de cible.

```bash
python3 Main.py
```

4. Le système commencera à contrôler la caméra PTZ en fonction des détections d'objet YOLO dans le flux vidéo. Vous pouvez observer le comportement du système en temps réel à l'aide du script `Test_ONVIF.py`.


---
