from ultralytics import YOLO
import  cv2
#import cvzone
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO('../YOLO Weights/yolov8n.pt')

# classNames = [
#     "person",
#     "bicycle",
#     "car",
#     "motorbike",
#     "aeroplane",
#     "bus",
#     "train",
#     "truck",
#     "boat",
#     "traffic light",
#     "fire hydrant",
#     "stop sign",
#     "parking meter",
#     "bench",
#     "bird",
#     "cat",
#     "dog",
#     "horse",
#     "sheep",
#     "cow",
#     "elephant",
#     "bear",
#     "zebra",
#     "giraffe",
#     "backpack",
#     "umbrella",
#     "handbag",
#     "tie",
#     "suitcase",
#     "frisbee",
#     "skis",
#     "snowboard",
#     "sports ball",
#     "kite",
#     "baseball bat",
#     "baseball glove",
#     "skateboard",
#     "surfboard",
#     "tennis racket",
#     "bottle",
#     "wine glass",
#     "cup",
#     "fork",
#     "knife",
#     "spoon",
#     "bowl",
#     "banana",
#     "apple",
#     "sandwich",
#     "orange",
#     "broccoli",
#     "carrot",
#     "hot dog",
#     "pizza",
#     "donut",
#     "cake",
#     "chair",
#     "sofa",
#     "pottedplant",
#     "bed",
#     "diningtable",
#     "toilet",
#     "tvmonitor",
#     "laptop",
#     "mouse",
#     "remote",
#     "keyboard",
#     "cell phone",
#     "microwave",
#     "oven",
#     "toaster",
#     "sink",
#     "refrigerator",
#     "book",
#     "clock",
#     "vase",
#     "scissors",
#     "teddy bear",
#     "hair drier",
#     "toothbrush"
# ]
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

def putTextRect(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, thickness=2, text_color=(255, 255, 255), rect_color=(0, 0, 0), offset=10):
    """
    Affiche du texte avec un rectangle de fond.

    :param img: Image sur laquelle dessiner
    :param text: Texte à afficher
    :param pos: Position (x, y) du coin inférieur gauche du texte
    :param font: Police du texte (OpenCV)
    :param scale: Échelle du texte
    :param thickness: Épaisseur des lettres
    :param text_color: Couleur du texte (BGR)
    :param rect_color: Couleur du rectangle (BGR)
    :param offset: Espace entre le texte et les bords du rectangle
    """
    
    # Obtenir la taille du texte et la ligne de base
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
    
    # Définir les coordonnées du rectangle
    x, y = pos
    rect_top_left = (x - offset, y - text_height - offset)
    rect_bottom_right = (x + text_width + offset, y + baseline + offset)
    
    # Dessiner le rectangle
    cv2.rectangle(img, rect_top_left, rect_bottom_right, rect_color, cv2.FILLED)
    
    # Dessiner le texte
    cv2.putText(img, text, (x, y), font, scale, text_color, thickness)


while True:
    success, img =cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2-x1, y2-y1
            # cvzone.cornerRect(img, (x1, y1, w, h))

            conf = math.ceil((box.conf[0]*100))/100

            cls = box.cls[0]
            name = classNames[int(cls)]

            # cvzone.putTextRect(img, f'{name} 'f'{conf}', (max(0,x1), max(35,y1)), scale = 0.5)
            putTextRect(img, f'{name} 'f'{conf}', (max(0,x1), max(35,y1)), scale=0.5, thickness=2, text_color=(255, 255, 255), rect_color=(0, 0, 0))


    cv2.imshow("Image", img)
    cv2.waitKey(1)



# Exemple d'utilisation
# if __name__ == "__main__":
#     # Charger une image
#     img = cv2.imread('image.jpg')
    
#     # Appeler la fonction pour ajouter du texte avec un rectangle de fond
#     putTextRect(img, "Hello World", (50, 100), scale=1, thickness=2, text_color=(255, 255, 255), rect_color=(0, 0, 0))
    
#     # Afficher l'image résultante
#     cv2.imshow('Image with Text', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
