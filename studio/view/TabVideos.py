from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivymd.utils import asynckivy
from studio.controller.CamController import CamController
from studio.controller.ExpansionPanel import FocusButton
from studio.enum.FormatEnum import FormatEnum
from studio.view.CamCapture import CamCapture
from kivymd.toast import toast
from threading import Thread
from studio.view.CamViewImage import CamViewImage


class CardScrollImage(MDCard):
    dropdown = None
    camController = CamController()
    app = None

    def __init__(self, app, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.app = app
    
    def on_start(self):
        asynckivy.start(self.on_start_video(self.text))
    
    async def on_start_video(self, text):
        await asynckivy.sleep(2)
        if self.camController.videoCamera:
            return toast("stopper d'abord la camera en cours.")
        await self.start_source(text)
    
    async def start_source(self, text):
        cam = None
        await asynckivy.sleep(2)
        for content in self.app.data.listCam:
            listText= content[0]
            if text == listText:
                cam = content[1]
                break
        lancer = await self.camController.add_start_video(text, self, cam, self.app)
        if lancer:
            print(f"start_source====>>>> {lancer}")
            if not self.app.data.camController.videoCamera:
                asynckivy.start(self.app.start_source(text))
            if not cam:
                self.app.data.listCam.append((text, lancer))
                if self.app.data.define_session:
                    insert_sql = "INSERT INTO camlists (cam_label, save, format, fk_session) VALUES (?, ?, ?, ?)"
                    self.app.data.db_manager.insert_data(insert_sql, (text, True, "", self.app.data.define_session[0]))
                

    def affiche_format(self):
        if not self.dropdown:
            self.dropdown = DropDown()
            for index in list(FormatEnum):

                btn = FocusButton(text=str(index.value), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.selectDropdown(btn.text))
                self.dropdown.add_widget(btn)
        self.dropdown.open(self.ids.label_format)
    
    def selectDropdown(self, text):
        self.dropdown.select(text)
        self.ids.label_format.text = "[color=#4287f5]format :" + str(text) + "[/color]"
        self.camController.select_format(text)
