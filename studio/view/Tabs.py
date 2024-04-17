from kivy.properties import ObjectProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.utils import asynckivy
from studio.view.CamCapture import CamCapture


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.''' 
    
    def on_text(self):
        text = self.ids.source.text
        if text:
            self.ids.spinner.active = True
            asynckivy.start(self.start_source(text))
        else:
            self.ids.spinner.active = False
    
    async def start_source(self, text):
        if not self.app.listCam[text]:
            await asynckivy.sleep(0.2)
            start_video = CamCapture(text, self)
            lancer = await start_video.lancer()
            if lancer:
                print(f"start_source====>>>> {lancer}")
                self.app.listCam.append((text, lancer))
        else:
            await asynckivy.sleep(0.2)
            start_video = CamCapture(text, self)
            lancer = await start_video.lancer(self.app.listCam[text])
        self.ids.spinner.active = False
