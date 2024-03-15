from Controle_ONVIF import OnvifPTZCamera
from DetectBird import tracking
from ultralytics import YOLO 
from time import time 
import json
import cv2

with open('Config.json', 'r') as fichier:
        config = json.load(fichier)

model = YOLO(config["yolo"]["model"],task='detect')

camera = OnvifPTZCamera(config["caméra"]["ip"], config["caméra"]["port"] ,config["caméra"]["login"], config["caméra"]["password"], config["caméra"]["verbose"])
camera.calibration()

player = cv2.VideoCapture(config["caméra"]["zoom"])

while player.isOpened():
    start_time = time()
    ret, frame = player.read()
    
    
    if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
        frame_224 = cv2.resize(frame, (224, 224))
        results = model.predict(frame_224, conf=config["yolo"]["confiance"],verbose=False, imgsz=224, max_det=1, vid_stride=5)
        tracking(camera, results[0], frame_224, config["tracking"]["vitesse"],config["tracking"]["tolérance"],config["tracking"]["target_label"],frame,config["tracking"]["capture_path"], config["tracking"]["verbose"])

        if config["yolo"]["display"] :
            res_plotted = results[0].plot()
            res_plotted = cv2.resize(res_plotted, (640, 640))
            cv2.imshow('Object Detection',res_plotted)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    end_time=time()
    if config["yolo"]["verbose"] : print("FPS :",1/(end_time-start_time))



player.release()
cv2.destroyAllWindows()
