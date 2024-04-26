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
