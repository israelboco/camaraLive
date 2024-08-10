import cv2
import numpy as np

# Chemins vers les fichiers YOLO
config_path = 'yolov3.cfg'
weights_path = 'yolov3.weights'
names_path = 'coco.names'

# Charger le modèle YOLO
net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def detect_objects(image_path):
    image = cv2.imread(image_path)
    height, width, channels = image.shape

    # Prétraitement de l'image
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

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

cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Détection dans le flux vidéo
    detected_objects = detect_objects(frame)
    
    # Affichage des objets détectés
    for box in detected_objects:
        x, y, w, h = box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
