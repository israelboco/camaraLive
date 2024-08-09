from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from ultralytics import YOLO
import cv2
import math
import time

class YoloApp(App):
    def build(self):
        # Create layout
        layout = BoxLayout(orientation='vertical')
        self.img_widget = Image()
        layout.add_widget(self.img_widget)
        
        # Process and update image
        self.process_and_display_image()
        
        return layout

    def process_and_display_image(self):
        # Load YOLO model
        model = YOLO('../YOLO Weights/yolov8n.pt')
        
        # Capture a single frame from the webcam
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        success, img = cap.read()
        #cap.release()
        
        while success:
            results = model(img, stream=True)
            classNames = ["personne", "vélo", "voiture", "moto", "avion", "bus", 
                          "train", "camion", "bateau", "feu de signalisation", "bouche d'incendie", 
                          "panneau d'arrêt", "parcmètre", "banc", "oiseau", "chat", "chien", 
                          "cheval", "mouton", "vache", "éléphant", "ours", "zèbre", "girafe", 
                          "sac à dos", "parapluie", "sac à main", "cravate", "valise", "frisbee", 
                          "skis", "snowboard", "ballon de sport", "cerf-volant", "batte de baseball", 
                          "gant de baseball", "planche à roulettes", "planche de surf", "raquette de tennis", 
                          "bouteille", "verre à vin", "tasse", "fourchette", "couteau", "cuillère", "bol", 
                          "banane", "pomme", "sandwich", "orange", "brocoli", "carotte", 
                          "hot-dog", "pizza", "donut", "gâteau", "chaise", "canapé", 
                          "plante en pot", "lit", "table à manger", "toilettes", "écran de télévision", 
                          "ordinateur portable", "souris", "télécommande", "clavier", "téléphone portable", 
                          "micro-ondes", "four", "grille-pain", "évier", "réfrigérateur", 
                          "livre", "horloge", "vase", "ciseaux", "ours en peluche", "sèche-cheveux", 
                          "brosse à dents"]

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = box.cls[0]
                    name = classNames[int(cls)]

                    self.draw_text_with_background(img, f'{name} {conf}', (max(0, x1), max(35, y1)))

            # Convert image to texture and update the widget
            buf = cv2.flip(img, 0).tostring()
            image_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img_widget.texture = image_texture
            time.sleep(50)


    def draw_text_with_background(self, img, text, pos, font_scale=0.5, thickness=1, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_w, text_h = text_size
        x, y = pos
        # Draw background rectangle
        cv2.rectangle(img, (x, y - text_h - 5), (x + text_w, y + 5), bg_color, -1)
        # Put the text on the image
        cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness)

if __name__ == "__main__":
    YoloApp().run()
