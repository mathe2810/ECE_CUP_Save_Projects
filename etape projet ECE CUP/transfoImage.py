import numpy as np
import cv2, PIL
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

import cv2


# # prendre 5 photos à partir de la webcam
#
# camera = cv2.VideoCapture(0)
# i = 0
# while i < 5:
#     input('Press Enter to capture')
#     return_value, image = camera.read()
#     cv2.imwrite('opencv' + str(i) + '.png', image)
#     i += 1
# del camera

# The cv2.aruco.detectMarkers
# results in a 3-tuple of:

# corners : The (x, y)-coordinates of our detected ArUco markers ids : The identifiers of the ArUco markers (i.e.,
# the ID encoded in the marker itself) rejected : A list of potential markers that were detected but ultimately
# rejected due to the code inside the marker not being able to be parsed

def form_square_from_arucos(corners):
    # Convertir les coins des marqueurs en un tableau numpy
    points = np.concatenate(corners, axis=0)

    # Trouver le rectangle englobant des points
    x, y, w, h = cv2.boundingRect(points)

    # Créer le carré englobant
    ordered_square = np.array([
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h)
    ])

    return ordered_square


# définir le dictionnaire de travail
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
# instancier le détecteur
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

image = cv2.imread('../image de test/img_1.png')

# stocker les arucos détectés : les positions de leurs coins, leur identifiants et les éventuelles erreurs
markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)

print(markerIds)
print(markerCorners)

Coord_Aruco_Carre = []
# verifier qu'au moins un aruco est détecté
if len(markerCorners) > 0:
    ids = markerIds.flatten()
    # boucle pour chaque aruco détecté
    for (markerCorner, markerID) in zip(markerCorners, ids):
        # extraire les angles des aruco (toujours dans l'ordre
        # haut-gauche, haut-droite, bas-gauche, bas-droit)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # convertir en entier (pour l'affichage)
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        # dessiner un quadrilatère autour de chaque aruco
        cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
        # calculer puis afficher un point rouge au centre
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
        # affiher l'identifiant
        cv2.putText(image, str(markerID),
                    (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        print("[INFO] ArUco marker ID: {}".format(markerID))
        # afficher l'image
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        Coord_Aruco_Carre.append(corners)

print(Coord_Aruco_Carre)

Coord_Aruco_Carre = form_square_from_arucos(Coord_Aruco_Carre)

print(Coord_Aruco_Carre)

cv2.polylines(image, [Coord_Aruco_Carre.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imshow("Image", image)
cv2.waitKey(0)

# Convertir les coordonnées en un format approprié
pts = np.array(Coord_Aruco_Carre, dtype=np.int32)
pts = pts.reshape((-1, 1, 2))

# Découper la région d'intérêt (ROI) à partir de l'image
roi = cv2.polylines(image.copy(), [pts], isClosed=True, color=(255, 0, 0), thickness=2)
roi = image[pts[0][0][1]:pts[2][0][1], pts[0][0][0]:pts[2][0][0]]

# Afficher la région d'intérêt (ROI)
cv2.imshow('Région d\'Intérêt (ROI)', roi)

cv2.waitKey(0)
cv2.destroyAllWindows()


# mesurons l'image
h, w = roi.shape[:2]
print('w = ' + str(w))
print('h = ' + str(h))
# specifions d'abord la positions de points dans la première image puis leurs position dans la nouvelle
points1 = np.float32(Coord_Aruco_Carre) #Avant changement --> [[268, 239], [514, 209], [350, 430], [600, 402]]
points2 = np.float32([[0, 100], [w, 0], [0, h], [w, h]])
# calculons une matrice de transformation
vecttrans = cv2.getPerspectiveTransform(points1, points2)
# appliquons la transformation à l'image d'orgine,spécifions un taille
finalimage = cv2.warpPerspective(roi, vecttrans, (w, h))
# displaying the original image and the transformed image as the output on the screen
cv2.imshow('Source_image', roi)
cv2.imshow('Destination_image', finalimage)
cv2.waitKey(0)
cv2.destroyAllWindows()
