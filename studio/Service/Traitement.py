import cv2
import numpy as np


class Traitement:
    # Chemins vers les fichiers YOLO
    #config_path = 'yolov3.cfg'
    #weights_path = 'yolov3.weights'
    #names_path = 'coco.names'
    config_path = ''
    weights_path = ''
    names_path = ''
    net = None
    layer_names = None
    output_layers = None


    def __init__(self, *args, **kwargs):
        # Charger le modèle YOLO
        try:
            self.net = cv2.dnn.readNet(self.weights_path, self.config_path)
            self.layer_names = self.net.getLayerNames()
            self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        except Exception as e:
            print(e)


    def object_dection(self, path):
        try:
            image = cv2.imread(path)
            height, width, channels = image.shape

            # Prétraitement de l'image
            blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outputs = self.net.forward(self.output_layers)

            class_ids = []
            confidences = []
            boxes = []

            # Traitement des résultats
            for output in outputs:
                for detection in output:
                    for obj in detection:
                        scores = obj[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            center_x = int(obj[0] * width)
                            center_y = int(obj[1] * height)
                            w = int(obj[2] * width)
                            h = int(obj[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)
                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

            indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            detected_objects = []
            for i in indices:
                i = i[0]
                box = boxes[i]
                detected_objects.append(box)

            return detected_objects

        except Exception as e:
            print(e)
            detected_objects = ""

        return detected_objects
    
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
