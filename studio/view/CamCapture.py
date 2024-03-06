import os
from datetime import datetime

import cv2
from kivy.clock import Clock
from kivy.core.image import Texture
from kivymd.utils import asynckivy

from studio.view.CameraFrame import Camera
from studio.view.MenuFrame import MenuBar


class CamCapture:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = 0
        self.screenMain = None
        self.videoCamera = None

        self.cameraVideo = Camera()
        self.mbar = MenuBar(self, self)

        # Initialiser l'enregistrement à False
        self.recording = False
        self.record_demarage = False
        # Liste pour stocker les images à enregistrer
        self.frames_to_record = []

    #        self.window.mainloop()

    def terminer(self):
        self.window.quit()

    def captureCamera(self):
        self.capture = 1

    def afert(self, delay, func):
        Clock.schedule_once(func, delay)
        # self.window.after(delay, func)

    def stop(self):
        # progress = ttk.Progressbar(self.window, length=400, maximum=300)
        # progress.pack(pady=30)
        # progress.start(10)
        self.recording = not self.recording
        self.frames_to_record = self.cameraVideo.enregistrer(self.frames_to_record)
        self.record_demarage = False

        # progress.stop()

    def enregistrer(self):
        self.recording = True
        print("Star record: " + str(self.recording))

    def lancer(self):
        if self.videoCamera is None:
            self.videoCamera = self.cameraVideo.afficheCamara(self.screenMain.lien.text)

        self.update()

    def update(self, dt=None):

        if self.videoCamera is not None:
            # Lire une image depuis le flux vidéo
            ret, frame = self.videoCamera.read()

            # Appeler récursivement la fonction update après un certain délai
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.screenMain.image_video.texture = image_texture
                if self.capture >= 1:
                    name = str(self.capture) + "_" + datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S")
                    self.save_frame_camera_key("enregistrement/capture", 'capture', name, frame)
                    self.capture += 1
                    print(self.capture)
                if self.capture == 100:
                    self.capture = 0

                # Enregistrer la frame si l'enregistrement est activé
                if self.recording:
                    self.frames_to_record.append(frame)
                    if not self.record_demarage:
                        self.record_demarage = not self.record_demarage
                        self.cameraVideo.record_demarage(self.frames_to_record)
                        self.record_update()

            # Appeler récursivement la fonction update après un certain délai
            # await self.afert(16, self.update())
            # self.window.after(16, func)
            time = 1 / 30
            self.afert(time, self.update)

    def record_update(self, dt=None):
        async def record_update():
            if self.recording and self.frames_to_record:
                await asynckivy.sleep(0)
                self.frames_to_record = self.cameraVideo.update_enregistrer(self.frames_to_record)
                self.afert(10, self.record_update)
                # self.window.after(15000, self.record_update)

        asynckivy.start(record_update())

    def stopCamera(self):
        self.recording = not self.recording
        self.frames_to_record = self.cameraVideo.enregistrer(self.frames_to_record)
        self.record_demarage = False

    def save_frame_camera_key(self, dir_path, basename, n, frame, ext='jpg'):
        # os.makedirs(dir_path, exist_ok=True)
        base_path = os.path.join(dir_path, basename)

        cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)