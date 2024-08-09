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
from kivy.clock import Clock
from kivy.core.image import Texture


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
    controle =None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )

    def start(self):
        pass

    def file_manager_open(self):
        
        path = filedialog.askopenfilename( 
            title="Ouvrir",
            defaultextension=".mp4",
            filetypes=(("Media files", "*.*"), ("All files", "*.*"))
        )
        # self.ids.image.source = path
        source = self.app.data.traitement.object_dection(path)
        try:
            if not source:
                self.ids.i_source.source = path
                return toast("Image invalide")
            print(source)
            buf1 = cv2.flip(source, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(source.shape[1], source.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.i_source.texture = image_texture
        except Exception as e:
            print(e)

    def select_path(self, path):
        self.exit_manager()
        print(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()


class MainScreenView(MDScreenManager):
    pass


class AProposBox(MDBoxLayout):
          
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog
    
    def open_cam(self):
        self.app.add_tab()
        self.dialog.dimiss()
