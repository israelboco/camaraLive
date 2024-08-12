import cv2
import math
#from ultralytics import YOLO
import numpy as np
from kivy.graphics.texture import Texture
from kivymd.utils import asynckivy
from kivy.clock import Clock
import time
from kivymd.toast import toast

class Traitement:
    
    def __init__(self):
        self.net = cv2.dnn.readNet("./config/yolov3.weights", "./config/yolov3.cfg")
        with open("./config/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.traints = []
        # Get files from openCV : https://github.com/opencv/opencv/tree/3.4/data/haarcascades
        self.classCascadefacial = cv2.CascadeClassifier("./config/haarcascade_frontalface_default.xml")   
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.gray_target = None
        self.encours = False
    
    async def person_detected(self, target):
        if not self.encours:
            toast('Personne trouvée')
            await asynckivy.sleep(1)
            toast('la cam est en cours de basculer')
            target.camController.on_switch()
            Clock.schedule_once(self.update_encour, 60)

    def update_encour(self, dt):
        self.encours = not self.encours
    
    def afert(self, delay, func, id):
        Clock.schedule_once(lambda dt: func(id, dt), delay)
    
    def start_traint(self, target):
        gry_target = self.profile_detection(target.detect_path)
        self.traints.append((target.id, target, gry_target))

    def stop_traints(self, target):
        self.traints.remove(target)
    
    def find_target(self, search_target):
        for id, target, gry_target in self.traints:
            if id == search_target:
                return (id, target, gry_target)
        return None
        
    # async def object_detection(self, path):
    #     try:
    #         img = cv2.imread(path)
    #         results = self.model(img, stream=True)
    #         for r in results:
    #             await asynckivy.sleep(0) 
    #             boxes = r.boxes
    #             for box in boxes:
    #                 x1, y1, x2, y2 = box.xyxy[0]
    #                 x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    #                 w, h = x2 - x1, y2 - y1
    #                 cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    #                 conf = math.ceil((box.conf[0] * 100)) / 100
    #                 cls = box.cls[0]
    #                 name = self.classNames[int(cls)]

    #                 # Préparation du texte
    #                 text = f'{name} {conf}'

    #                 # Calcul de la largeur et de la hauteur du texte
    #                 (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

    #                 # Dessiner le rectangle de fond pour le texte
    #                 cv2.rectangle(img, (x1, y1 - text_height - 10), (x1 + text_width, y1), (0, 255, 0), -1)

    #                 # Placer le texte au-dessus du rectangle
    #                 cv2.putText(img, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    #         # Conversion de l'image OpenCV en texture Kivy
    #         buf1 = cv2.flip(img, 0)
    #         buf = buf1.tobytes()
    #         image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
    #         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    #         return image_texture

    #     except Exception as e:
    #         print("object_detection ===>")
    #         print(e)
    #     return None


    async def object_dectionz(self, path):
        try:
            # Charger l'image fournie
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            height, width = image.shape[:2]
            # Initialiser le détecteur ORB (ou utiliser SIFT/SURF si disponible)
            blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)

            layer_names = self.net.getLayerNames()
            output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
            outs = self.net.forward(output_layers)
            boxes = []
            class_ids = []
            confidences = []
            for out in outs:
                await asynckivy.sleep(0)
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

                indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

                for i in indices:
                    await asynckivy.sleep(0)
                    i = i[0]
                    box = boxes[i]
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    label = str(self.classes[class_ids[i]])
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Conversion de l'image OpenCV en texture Kivy
            buf1 = cv2.flip(image, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            return image_texture

        except Exception as e:
            print("object_detectionz ===>")
            print(e)

        return None

    def start(self, id=None, dt=None):
        controle = self.find_target(id)
        if not controle:
            return
        print("demare recherche")
        asynckivy.start(self.start_controle(controle))
 
    async def start_controle(self, controle):
        print(controle)
        id, target, gray_target = controle

        if target.camController.videoCamera and target.type_personne:
            # Lire une image depuis le flux vidéo
            ret, frame = target.camController.videoCamera.read()
            # Appeler récursivement la fonction update après un certain délai
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.classCascadefacial.empty():
                    print("Erreur : Le classificateur facial n'a pas été chargé correctement.")
                    return
                # faces = self.classCascadefacial.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
                faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                profiles = self.profile_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                eyes = self.eye_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))
                for (x, y, w, h) in faces:
                    await asynckivy.sleep(0)
                    roi = gray_frame[y:y+h, x:x+w]
                    result_face = cv2.matchTemplate(roi, gray_target, cv2.TM_CCOEFF_NORMED)
                    result_profile = cv2.matchTemplate(roi, gray_target, cv2.TM_CCOEFF_NORMED)
                    result_eyes = cv2.matchTemplate(roi, gray_target, cv2.TM_CCOEFF_NORMED)
                    min_val_face, max_val_face, min_loc_face, max_loc_face = cv2.minMaxLoc(result_face)
                    min_val_profile, max_val_profile, min_loc_profile, max_loc_profile = cv2.minMaxLoc(result_profile)
                    min_val_eyes, max_val_eyes, min_loc_eyes, max_loc_eyes = cv2.minMaxLoc(result_eyes)
                    if max_val_face > 0.8 and max_val_profile > 0.8 and max_val_eyes > 0.8:
                        await self.person_detected(target)
                    top_left = max_loc_face
                    h, w = gray_target.shape
                    bottom_right = (top_left[0] + w, top_left[1] + h)
                    cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    self.gray_target = frame
                    
                self.afert(1, self.start, target.id)


    def facialDetectionAndMark(self, _image, _classCascade):
        imgreturn = _image.copy()
        gray = cv2.cvtColor(imgreturn, cv2.COLOR_BGR2GRAY)
        faces = _classCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(imgreturn, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return imgreturn

    def profile_detection(self, path):
        self.target_image = cv2.imread(path)
        self.gray_target = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2GRAY)
        return self.gray_target
