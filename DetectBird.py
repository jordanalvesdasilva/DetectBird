from enum import Enum
import datetime
import numpy
import cv2 
import os 
from time import time 



class Direction(Enum):
    NEUTRE = 'neutre'
    GAUCHE = 'gauche'
    DROITE = 'droite'
    HAUT = 'haut'
    BAS = 'bas'
    
ma_direction = Direction.NEUTRE
calibration=0
calibration_flag=False
target_present_history = [False] * 30


def capture_image_from_stream(capture, name, capture_path):
    """
    Capture une image à partir du flux vidéo et l'enregistre.

    :param capture: Image capturée à enregistrer.
    :param name: Nom de l'image.
    :param capture: Chemin d'enregistrement.

    __
    """

    os.makedirs(capture_path, exist_ok=True)

    current_datetime = datetime.datetime.now()
    datetime_format = current_datetime.strftime("%Y-%m-%d_%H:%M:%S")
    output_image_path = capture_path + "/" +  name + "_" + datetime_format + ".jpg"

    cv2.imwrite(output_image_path, capture)


def tracking(camera, results, frame, speed, tolerance, target_label, capture, capture_path, verbose=False):
    """
    Effectue le suivi de la cible dans le flux vidéo.

    :param camera: Instance de la caméra utilisée pour le suivi.
    :param results: Résultats de la détection de la cible.
    :param frame: Image actuelle du flux vidéo.
    :param speed: Vitesse de déplacement de la caméra.
    :param tolerance: Tolérance pour considérer la cible comme centrée.
    :param target_label: Étiquette de la cible à suivre.
    :param capture: Instance de capture vidéo.
    :param verbose: Flag pour activer les messages verbeux.

    __
    """
    target_present = False
    global ma_direction
    global zoom
    global calibration
    global calibration_flag
    global target_present_history
    
    box = results.boxes.cpu()
    box_sz = box.xyxy.numpy()
    if box.cls.nelement() > 0:
        label = int(box.cls[0].item()) 
        if label == target_label:
            calibration -=1
            if calibration > 0 :
                calibration =0
            if calibration < -10 :
                calibration_flag=True
                calibration=0
            target_present = True
            frame_shape_x, frame_shape_y = frame.shape[1], frame.shape[0]
            frame_center_x,frame_center_y = frame_shape_x//2 , frame_shape_y//2
            x1, x2 = int(box_sz[0,0]), int(box_sz[0,2])
            y1, y2 = int(box_sz[0,1]), int(box_sz[0,3])
            x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2
            dx = x_center - frame_center_x
            dy = y_center - frame_center_y
            norm_dx = dx / frame_shape_x
            norm_dy = dy / frame_shape_y

            # Vérifie si l'objet est suffisamment proche du centre
            if abs(norm_dx) > tolerance or abs(norm_dy) > tolerance:
                if abs(norm_dx) > tolerance  :
                    if norm_dx > tolerance/2 and ma_direction != Direction.DROITE:
                        if verbose: print("Tourner à DROITE avec l'ancienne direction",ma_direction)
                        camera.right(speed)
                        ma_direction = Direction.DROITE

                    elif norm_dx < -tolerance/2 and ma_direction != Direction.GAUCHE:
                        if verbose: print("Tourner à GAUCHE avec l'ancienne direction",ma_direction)
                        camera.left(speed)
                        ma_direction = Direction.GAUCHE

                elif abs(norm_dy) > tolerance:
                    if norm_dy > tolerance/2 and ma_direction != Direction.BAS:
                        if verbose: print("Tourner vers le BAS avec l'ancienne direction",ma_direction)
                        camera.down(speed)
                        ma_direction = Direction.BAS
                    elif norm_dy < tolerance/2 and ma_direction != Direction.HAUT:
                        if verbose: print("Tourner vers le HAUT avec l'ancienne direction",ma_direction)
                        camera.up(speed)
                        ma_direction = Direction.HAUT

            
            elif ma_direction != Direction.NEUTRE:
                camera.stop_movement()
                if verbose: print("Arret objet au centre") 
                ma_direction = Direction.NEUTRE
            

    target_present_history.append(target_present)
    target_present_history = target_present_history[-10:]
    if all(target_present_history):
        start_time = time()
        capture_image_from_stream(capture,"Image_Grand_Angle",capture_path)
        end_time = time()
        print(end_time-start_time)
        if verbose: print("Image grand angle capturée")


    if not target_present:
        calibration+=1
        if calibration > 1000 :
            calibration=0
            if calibration_flag == True:
                camera.calibration()
                calibration_flag=False
        if ma_direction != Direction.NEUTRE :
            camera.stop_movement()
            if verbose: print("Arret perte de précense",ma_direction)
            ma_direction = Direction.NEUTRE
            
            
        
