import cv2
import numpy as np
import keyboard
import time


def on_key_event(e):
    if e.name == 'esc':
        print("Touche ESC pressée. Arrêt du programme.")
        keyboard.unhook_all()


# Définir le dictionnaire ArUco (par exemple, DICT_4X4_50)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
# ID du marqueur ArUco
marker_id = 0


# Taille du marqueur ArUco
marker_size = 300
# Générer le marqueur ArUco

while 1:
    print(marker_id)
    marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    marker_id += 1
    if marker_id > 49:
        marker_id = 0
    # Afficher le marqueur généré
    if keyboard.is_pressed("esc"):
        break
    if keyboard.is_pressed("p"):
        cv2.imwrite("./image aruco/" + 'Aruco_id_' + str(marker_id-1) + "_dict_" + "DICT_4X4_250" + '.png', marker_img)
        print("saved")
    cv2.imshow('ArUco Marker', marker_img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
