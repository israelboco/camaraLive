import cv2
import numpy as np


class Traitement:

    def object_dection(self, path):
        # Charger l'image de référence
        image_ref = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        blurred = cv2.GaussianBlur(image_ref, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # Trouver les contours dans l'image de référence
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image_ref, None)


    def start(self):
        # Initialisation de la capture vidéo
        cap = cv2.VideoCapture(0)

        # Initialisation du détecteur de mouvement
        fgbg = cv2.createBackgroundSubtractorMOG2()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Conversion de l'image en niveaux de gris
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Appliquer le détecteur de mouvement
            fgmask = fgbg.apply(gray)
            
            # Trouver les contours des objets détectés
            contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue
                
                # Dessiner un rectangle autour des objets détectés
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Afficher le flux vidéo avec les objets suivis
            cv2.imshow('Frame', frame)
            cv2.imshow('FG Mask', fgmask)
            
            # Quitter la boucle quand 'q' est pressé
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

# Libérer les ressources
#cap.release()
#cv2.destroyAllWindows()
