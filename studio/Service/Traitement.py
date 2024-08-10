import cv2
import math
from ultralytics import YOLO
import numpy as np
from kivy.graphics.texture import Texture
from kivymd.utils import asynckivy
from kivy.clock import Clock

class Traitement:
 
    model = YOLO('../YOLO Weights/yolov8n.pt')
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", 
              "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter",
              "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear",
              "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase",
              "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
              "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
              "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", 
              "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", 
              "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone", 
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", 
              "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
            ]
    
    def __init__(self):
        self.traints = []
        self.dirCascadeFiles = r'../opencv/haarcascades_cuda/'
        # Get files from openCV : https://github.com/opencv/opencv/tree/3.4/data/haarcascades
        self.classCascadefacial = cv2.CascadeClassifier(self.dirCascadeFiles + "haarcascade_frontalface_default.xml")   
        
        # Chemins vers les fichiers YOLO
        self.config_path = 'yolov3.cfg'
        self.weights_path = 'yolov3.weights'
        self.names_path = 'coco.names'

        # Charger le modèle YOLO
        self.net = cv2.dnn.readNet(self.weights_path, self.config_path)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.encours = False
    
    def person_detected(self, target):
        if not self.encours:
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
        
    async def object_detection(self, path):
        try:
            img = cv2.imread(path)
            results = self.model(img, stream=True)
            for r in results:
                await asynckivy.sleep(0) 
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = box.cls[0]
                    name = self.classNames[int(cls)]

                    # Préparation du texte
                    text = f'{name} {conf}'

                    # Calcul de la largeur et de la hauteur du texte
                    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    # Dessiner le rectangle de fond pour le texte
                    cv2.rectangle(img, (x1, y1 - text_height - 10), (x1 + text_width, y1), (0, 255, 0), -1)

                    # Placer le texte au-dessus du rectangle
                    cv2.putText(img, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

            # Conversion de l'image OpenCV en texture Kivy
            buf1 = cv2.flip(img, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            return image_texture

        except Exception as e:
            print("object_detection ===>")
            print(e)
        return None


    async def object_dectionz(self, path):
        try:
            # Charger l'image fournie
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            await asynckivy.sleep(0)
            # Initialiser le détecteur ORB (ou utiliser SIFT/SURF si disponible)
            orb = cv2.ORB_create()
            await asynckivy.sleep(0)
            # Trouver les points clés et les descripteurs dans l'image
            keypoints, descriptors = orb.detectAndCompute(image, None)

            # Afficher les points clés détectés
            image_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0))
        
            buf1 = cv2.flip(image_keypoints, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(image_keypoints.shape[1], image_keypoints.shape[0]), colorfmt='bgr')
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
        asynckivy.start(self.start_controle(controle))
 
    async def start_controle(self, controle):
        target = controle[1]
        gray_target = controle[2]
        if target.camController.videoCamera and target.type_personne:
            # Lire une image depuis le flux vidéo
            ret, frame = target.camController.videoCamera.read()
            # Appeler récursivement la fonction update après un certain délai
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.classCascadefacial.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
                for (x, y, w, h) in faces:
                    roi = gray_frame[y:y+h, x:x+w]
                    result = cv2.matchTemplate(roi, gray_target, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if max_val > 0.8:
                        self.person_detected(target)
                    top_left = max_loc
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
