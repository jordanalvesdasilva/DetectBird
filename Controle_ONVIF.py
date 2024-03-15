from onvif import ONVIFCamera
from zeep.transports import Transport
import ssl
import requests
import time
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# https://agsh.github.io/onvif/

class OnvifPTZCamera:
    def __init__(self, ip, port, username, password, verbose=False):
        """
        Initialise une instance de OnvifPTZCamera.

        :param ip: Adresse IP de la caméra.
        :param port: Port utilisé pour la connexion ONVIF.
        :param username: Nom d'utilisateur pour l'authentification.
        :param password: Mot de passe pour l'authentification.

        Désactive la vérification de certificat SSL et initialise les services média et PTZ.

        __
        """
        session = requests.Session()
        session.verify = False  # Désactiver la vérification de certificat
        transport = Transport(session=session)

        self.camera = ONVIFCamera(ip, port, username, password, transport=transport)
        self.media_service = self.camera.create_media_service()
        self.ptz_service = self.camera.create_ptz_service()
        self.profile = self.media_service.GetProfiles()[0]
        self.verbose = verbose


    def _move_ptz(self, pan_speed=0, tilt_speed=0, zoom_speed=0):
        """
        Effectue un mouvement PTZ en fonction des vitesses spécifiées.

        :param pan_speed: Vitesse de panoramique (gauche/droite).
        :param tilt_speed: Vitesse d'inclinaison (haut/bas).
        :param zoom_speed: Vitesse de zoom.

        __
        """
        request = self.ptz_service.create_type('ContinuousMove')
        request.ProfileToken = self.profile.token
        request.Velocity = {
            'PanTilt': {'x': pan_speed, 'y': tilt_speed},
            'Zoom': {'x': zoom_speed}
        }
        self.ptz_service.ContinuousMove(request)

    def stop_movement(self):
        """
        Arrête tout mouvement de la caméra PTZ.
        """
        self.ptz_service.Stop({'ProfileToken': self.profile.token})
        if self.verbose: print("Mouvement de la caméra arrêté avec succès.")

    def left(self, speed=1):
        """
        Déplace la caméra vers la gauche.

        :param speed: Vitesse du déplacement.

        __
        """
        self._move_ptz(pan_speed=-speed)
        if self.verbose: print("Commande GAUCHE envoyée avec succès.")

    def right(self, speed=1):
        """
        Déplace la caméra vers la droite.

        :param speed: Vitesse du déplacement.

        __
        """
        self._move_ptz(pan_speed=speed)
        if self.verbose: print("Commande DROITE envoyée avec succès.")

    def up(self, speed=1):
        """
        Déplace la caméra vers le haut.

        :param speed: Vitesse du déplacement.

        __
        """
        self._move_ptz(tilt_speed=speed)
        if self.verbose: print("Commande HAUT envoyée avec succès.")

    def down(self, speed=1):
        """
        Déplace la caméra vers le bas.

        :param speed: Vitesse du déplacement.

        __
        """
        self._move_ptz(tilt_speed=-speed)
        if self.verbose: print("Commande BAS envoyée avec succès.")

    def zoom(self, speed=1):
        """
        Effectue un zoom avant.

        :param speed: Vitesse du zoom.

        __
        """
        self._move_ptz(zoom_speed=speed)
        if self.verbose: print("Commande ZOOM envoyée avec succès.")

    def dezoom(self, speed=1):
        """
        Effectue un zoom arrière.

        :param speed: Vitesse du zoom.

        __
        """
        self._move_ptz(zoom_speed=-speed)
        if self.verbose: print("Commande DEZOOM envoyée avec succès.")

    def calibration(self):
        """
        Déplace la caméra vers une position neutre centrale.

        __
        """
        self.up()
        time.sleep(3)
        self.stop_movement()
        self.down()
        time.sleep(0.2)
        self.stop_movement()

        self.left()
        time.sleep(4)
        self.stop_movement()
        self.right()
        time.sleep(1.875)
        self.stop_movement()

        for i in range (50) : 
            self.zoom() 
        

        if self.verbose: print("Calibration effectuée : caméra déplacée vers la position neutre.")


# Utilisation
if __name__ == "__main__":
    camera = OnvifPTZCamera("192.168.0.3", 8000, "admin", "ptz909090",False)
    # camera.calibration()
    for i in range (50) : 
            camera.zoom()


