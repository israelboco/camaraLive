from kivy.properties import ObjectProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivymd.utils import asynckivy
from studio.enum.FormatEnum import FormatEnum
from studio.view.CamCapture import CamCapture


class TabVideo(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.''' 
    dropdown = None

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    
    def on_start_video(self):
        text = self.ids.source.text
        if text:
            self.ids.spinner.active = True
            asynckivy.start(self.start_source(text))
        else:
            self.ids.spinner.active = False
    
    async def start_source(self, text):
        cam = None
        for content in self.app.listCam:
            print(content)
            listText, cam = content
            if text == listText:
                break
        if not cam:
            await asynckivy.sleep(0.2)
            start_video = CamCapture(text, self)
            lancer = await start_video.lancer()
            if lancer:
                print(f"start_source====>>>> {lancer}")
                self.app.listCam.append((text, lancer))
        else:
            await asynckivy.sleep(0.2)
            start_video = CamCapture(text, self)
            lancer = await start_video.lancer(cam)
        self.ids.spinner.active = False

    def on_start_audio(self):
        pass

    def affiche_format(self):
        if not self.dropdown:
            self.dropdown = DropDown()
            for index in list(FormatEnum):

                btn = Button(text=str(index.value), size_hint_y=None, height=44)
                # btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(btn)
        self.dropdown.open(self.ids.source)
    