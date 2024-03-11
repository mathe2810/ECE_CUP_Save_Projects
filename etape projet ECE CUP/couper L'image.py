import cv2
import numpy as np


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


# Exemple d'utilisation avec des coordonnées de coins de marqueurs ArUco
# Assurez-vous d'ajuster les coordonnées en entrée selon vos besoins.
corners_aruco1 = np.array([(100, 100), (200, 100), (200, 200), (100, 200)])
corners_aruco2 = np.array([(300, 100), (400, 100), (400, 200), (300, 200)])
corners_aruco3 = np.array([(400, 100), (500, 100), (500, 200), (400, 200)])
corners_aruco4 = np.array([(100, 300), (100, 400), (200, 400), (200, 300)])
# Obtenir les coordonnées ordonnées du carré à partir des marqueurs ArUco
ordered_square = form_square_from_arucos([corners_aruco1, corners_aruco2, corners_aruco3, corners_aruco4])

print("Coordonnées ordonnées du carré :\n", ordered_square)

# Dimensions de l'image (par exemple, 800x600 pixels)
largeur, hauteur = 800, 600

# Créer une image blanche
image_blanche = np.ones((hauteur, largeur, 3), dtype=np.uint8) * 255

# Utiliser les coordonnées ordonnées du carré avec cv2.polylines
cv2.polylines(image_blanche, [ordered_square.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)

# Dessiner le premier carré (corners_aruco1) en bleu
cv2.polylines(image_blanche, [corners_aruco1.astype(int)], isClosed=True, color=(255, 0, 0), thickness=1)

# Dessiner le deuxième carré (corners_aruco2) en noir
cv2.polylines(image_blanche, [corners_aruco2.astype(int)], isClosed=True, color=(0, 0, 0), thickness=1)

# Afficher l'image blanche (optionnel)
cv2.imshow('Image Blanche', image_blanche)
cv2.waitKey(0)
cv2.destroyAllWindows()
