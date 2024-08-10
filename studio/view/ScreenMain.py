from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from studio.Service.NotificationService import NotificationService
from tkinter import filedialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import cv2
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivy.core.image import Texture
from kivymd.utils import asynckivy

from studio.constants.GetNetworks import GetNetworks


class ScreenMain(MDScreen):
    notificationService = NotificationService()

    def callWelcome(self):
        self.main_view.transition.direction = "left"
        self.main_view.current = "screen welcome"
    
    def dialog_box_cam(self):
        self.notificationService.add_cam_box()

class ScreenWelcome(MDScreen):
    dialog = None
    
    def apropos(self):
        text = '[i][color=#5AA6FF]Meilleure application pour optimiser la capture et la diffusion multi-sources en temps réel lors d\'événements : une solution rentable avec Cam Live.[/i][/color]'
        if not self.dialog:
                self.dialog = MDDialog(
                    title='[b][color=#5AA6FF]A propos[/color][/b]',
                    type="custom",
                    content_cls=AProposBox(),
                    md_bg_color="#262626",
                )
                self.dialog.content_cls.label_propos.text = text
                self.dialog.open()


class CardViewImage(MDCard):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
               

class CardReducteImage(MDCard, FocusBehavior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controle = None
        self.ids.check_person.active = True
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )
        self.getnetworks = GetNetworks()
        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index["interface"]),
                "trailing_icon": str(index["trailing_icon"]),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_camera, width_mult=3, caller=self.ids.list_camera)


    def start(self):
        self.ids.lien.text = self.controle.text
        if self.controle.detect_path:
            self.ids.i_source.texture = self.controle.detect_path
            self.ids.check_person.active = True
    
    def listcamera(self):
       self.dropdown2.open()

    def on_start_video(self):
        asynckivy.start(self.controle.on_start_video(self.ids.lien.text))

    def on_checkbox_active(self, type, active):
        print(type)
        print(active)
        if type == "Objet":
            self.controle.type_objet = True
            self.controle.type_personne = False
        if type == "Personne":
            self.controle.type_objet = False
            self.controle.type_personne = True

    def file_manager_open(self):
        if not self.controle.type_personne:
            return toast("Select Personne")
        
        path = filedialog.askopenfilename( 
            title="Ouvrir",
            defaultextension=".jpg",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"), ("All files", "*.*"))
        )
        self.ids.i_source.texture = path
        self.controle.detect_path = path

    def detect_object(self, dt):
        asynckivy.start(self.detect_object_async())
    
    async def detect_object_async(self):
        # self.ids.image.source = path
        if self.controle.camController.videoCamera:
            # Lire une image depuis le flux vidéo
            ret, frame = self.controle.camController.videoCamera.read()
            # Appeler récursivement la fonction update après un certain délai
            if ret:
                source = await self.app.data.traitement.object_detection(frame)
                try:
                    if not source:
                        self.ids.i_source.source = frame
                        return toast("Echec du traitement")
                    self.ids.i_source.texture = source
                except Exception as e:
                    print("file_manager_open ===>")
                    print(e)
            if self.controle.type_objet:
                self.afert(5, self.detect_object)
    
    def lancerTraitement(self):
        if self.controle.type_objet and self.ids.lancer.text == "Lancer":
            self.controle.type_persenne = False
            self.detect_object()
        if self.controle.type_persenne and self.ids.lancer.text == "Lancer":
            self.controle.type_persenne = False
            self.controle.start_traint = True
            self.app.data.traitement.start_traint(self.controle)
            asynckivy.start(self.app.data.traitement.start(self.controle.id))
        if self.ids.lancer.text == "Lancer":
            self.ids.lancer.text = "Annuler"
        else:
            self.ids.lancer.text = "Lancer"
            self.controle.start_traint = False

    def afert(self, delay, func):
        Clock.schedule_once(func, delay)

    def select_path(self, path):
        self.exit_manager()
        print(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()


class MainScreenView(MDScreenManager):
    pass


class AProposBox(MDBoxLayout):
          
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
