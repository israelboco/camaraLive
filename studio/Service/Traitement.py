import cv2
import math
from ultralytics import YOLO
import numpy as np

class Traitement:

    model = YOLO('../YOLO Weights/yolov8n.pt')
    classNames = [
        "personne",
        "vélo",
        "voiture",
        "moto",
        "avion",
        "bus",
        "train",
        "camion",
        "bateau",
        "feu de circulation",
        "bouche d'incendie",
        "panneau d'arrêt",
        "parcmètre",
        "banc",
        "oiseau",
        "chat",
        "chien",
        "cheval",
        "mouton",
        "vache",
        "éléphant",
        "ours",
        "zèbre",
        "girafe",
        "sac à dos",
        "parapluie",
        "sac à main",
        "cravate",
        "valise",
        "frisbee",
        "skis",
        "snowboard",
        "ballon de sport",
        "cerf-volant",
        "batte de base-ball",
        "gant de baseball",
        "skateboard",
        "planche de surf",
        "raquette de tennis",
        "bouteille",
        "verre à vin",
        "tasse",
        "fourchette",
        "couteau",
        "cuillère",
        "bol",
        "banane",
        "pomme",
        "sandwich",
        "orange",
        "brocoli",
        "carotte",
        "hot-dog",
        "pizza",
        "beignet",
        "gâteau",
        "chaise",
        "canapé",
        "plante en pot",
        "lit",
        "table à manger",
        "toilettes",
        "écran de télévision",
        "ordinateur portable",
        "souris",
        "télécommande",
        "clavier",
        "téléphone portable",
        "micro-ondes",
        "four",
        "grille-pain",
        "évier",
        "réfrigérateur",
        "livre",
        "horloge",
        "vase",
        "ciseaux",
        "ours en peluche",
        "sèche-cheveux",
        "brosse à dents"
    ]

    def object_dection(self, path):
        try:
            img = cv2.imread(path)
            results = self.model(img, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = box.cls[0]
                    name = self.classNames[int(cls)]

                    # Prepare text
                    text = f'{name} {conf}'

                    # Calculate text width & height
                    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    # Draw filled rectangle background for text
                    cv2.rectangle(img, (x1, y1 - text_height - 10), (x1 + text_width, y1), (0, 255, 0), -1)

                    # Put text above the rectangle
                    cv2.putText(img, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

            return img

        except Exception as e:
            print(e)
            img = None

        return img
    
    def object_dectionz(self, path):
        try:
            # Charger l'image fournie
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

            # Initialiser le détecteur ORB (ou utiliser SIFT/SURF si disponible)
            orb = cv2.ORB_create()

            # Trouver les points clés et les descripteurs dans l'image
            keypoints, descriptors = orb.detectAndCompute(image, None)

            # Afficher les points clés détectés
            image_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0))
        except Exception as e:
            print(e)
            image_keypoints = ""

        return image_keypoints


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
