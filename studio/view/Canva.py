import cv2
import tkinter as tk
from PIL import Image, ImageTk


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        # Ouvrir le flux vidéo
        self.cap = cv2.VideoCapture(video_source)

        # Créer une Frame Tkinter pour afficher la vidéo
        self.canvas = tk.Canvas(window, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        # Bouton pour commencer/arrêter l'enregistrement
        self.record_button = tk.Button(window, text="Enregistrer", command=self.toggle_record)
        self.record_button.pack(pady=10)

        # Initialiser l'enregistrement à False
        self.recording = False

        # Liste pour stocker les images à enregistrer
        self.frames_to_record = []

        # Mettre à jour la vidéo dans la Frame
        self.update()

        self.window.mainloop()

    def update(self):
        # Lire une image depuis le flux vidéo
        ret, frame = self.cap.read()

        if ret:
            # Convertir l'image OpenCV en format Tkinter
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image=image)

            # Mettre à jour l'image dans la Frame
            self.canvas.image = image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)

            # Enregistrer la frame si l'enregistrement est activé
            if self.recording:
                self.frames_to_record.append(frame)

        # Appeler récursivement la fonction update après un certain délai
        self.window.after(10, self.update)

    def toggle_record(self):
        # Basculer l'état d'enregistrement
        self.recording = not self.recording

        # Commencer ou arrêter l'enregistrement
        if self.recording:
            self.record_button.config(text="Arrêter l'enregistrement")
        else:
            self.record_button.config(text="Commencer l'enregistrement")

            # Enregistrer la liste d'images en vidéo
            if self.frames_to_record:
                height, width, layers = self.frames_to_record[0].shape
                size = (width, height)
                out = cv2.VideoWriter('enregistrement.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

                for i in range(len(self.frames_to_record)):
                    out.write(self.frames_to_record[i])

                out.release()
                self.frames_to_record = []


# Créer une instance de la classe App avec le numéro du périphérique vidéo
App(tk.Tk(), "Tkinter avec Vidéo OpenCV", video_source=0)
