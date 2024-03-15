import cv2
import time
from Controle_ONVIF import OnvifPTZCamera
from multiprocessing import Process
from DetectBird import capture_image_from_stream
import datetime
import json

def test_vidéo(URL):
    """
    Affiche le flux vidéo en utilisant OpenCV.

    :param URL: L'URL du flux vidéo.

    :return: Aucune valeur de retour.

    __
    """
    cap = cv2.VideoCapture(URL)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir le flux vidéo.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire la vidéo.")
            break
        cv2.imshow('Stream', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def test_contrôle_vidéo(URL, ip, port, login, password):
    """
    Contrôle une caméra et affiche le flux vidéo en utilisant OpenCV.

    :param URL: L'URL du flux vidéo.

    :return: Aucune valeur de retour.

    __
    """
    camera = OnvifPTZCamera(ip,port,login,password)
    cap = cv2.VideoCapture(URL)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir le flux vidéo.")
        return
    
    last=None
    no_key_pressed_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire la vidéo.")
            break

        cv2.imshow('Stream', frame)

        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == 82 and last != 'up':# Flèche haut
            camera.up(speed=32)
            last = 'up'
            no_key_pressed_count = 0
        elif key == 84 and last != 'down':  # Flèche bas
            camera.down(speed=32)
            last = 'down'
            no_key_pressed_count = 0
        elif key == 83 and last != 'right': # Flèche droite
            camera.right(speed=1)
            last = 'right'
            no_key_pressed_count = 0
        elif key == 81 and last != 'left':  # Flèche gauche
            camera.left(speed=1)
            last = 'left'
            no_key_pressed_count = 0
        elif key == ord('d') and last != 'dezoom':  # Lettre D
            camera.dezoom(speed=32)  # Utilisation de la fonction zoom_out corrigée
            last = 'dezoom'
            no_key_pressed_count = 0
        elif key == ord('z') and last != 'zoom':  # Lettre Z
            camera.zoom(speed=32)  # Utilisation de la fonction zoom_in corrigée
            last = 'zoom'
            no_key_pressed_count = 0
        elif key == ord('c') and last != 'calibration':  # Lettre C
            camera.calibration()
            last = 'calibration'   
            no_key_pressed_count = 0
        elif key == ord('r') and last != 'Capture':  # Lettre R
            capture_image_from_stream("frame","Image_Test")
            last = 'Capture'   
            no_key_pressed_count = 0      
        elif key == 255:  # Aucune touche n'est appuyée
            no_key_pressed_count += 1
            if no_key_pressed_count >= 5 and last in ['down','up', 'left','right','zoom','dezoom']:
                last = None
                camera.stop_movement()
        
        
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    with open('Config.json', 'r') as fichier:
        config = json.load(fichier)


    # Créer deux processus pour afficher les flux vidéo en parallèle
    process1 = Process(target=test_contrôle_vidéo, args=(config["caméra"]["zoom"],config["caméra"]["ip"], config["caméra"]["port"] ,config["caméra"]["login"], config["caméra"]["password"],))
    process2 = Process(target=test_vidéo, args=(config["caméra"]["grand_angle"],))

    process1.start()
    process2.start()

    process1.join()
    process2.join()