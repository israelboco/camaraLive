from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.font_definitions import fonts
from kivymd.uix.screen import MDScreen
from kivymd.utils import asynckivy

from studio.view.CamCapture import CamCapture
from studio.view.CameraFrame import Camera
from studio.view.CardAudio import CardAudio
from studio.view.MenuFrame import MenuBar
from studio.view.MyProcess import MyProcess
from studio.view.ScreenMain import ScreenMain
from studio.view.Tabs import Tab
from kivymd.icon_definitions import md_icons

Builder.load_file("studio/view/kv/main.kv")


class AppCameraLive(MDApp):
    index = 1
    listProces = []

    def build(self) -> MDScreen:
        self.title = "Camera Live"
        self.screenMain = ScreenMain()
        return self.screenMain

    def on_start(self):
        tab = Tab(id='1', title="CamLive 1")
        self.root.ids.tabs.add_widget(tab)
        CamCapture(tab)

    def on_stop(self):
        pass

    def add_tab(self):
        self.index += 1
        name_tab = f"CamLive {self.index}"
        tab = Tab(
            id=str(self.index),
            tab_label_text=f"[ref={name_tab}][font={fonts[-1]['fn_regular']}]{md_icons['close']}[/font][/ref]{name_tab}"
        )
        self.root.ids.tabs.add_widget(
             tab
        )
        CamCapture(tab)

    def remove_tab(self):
        if self.index > 1:
            self.index -= 1
        self.root.ids.tabs.remove_widget(
            self.root.ids.tabs.get_tab_list()[-1]
        )

    def on_ref_press(
            self,
            instance_tabs,
            instance_tab_label,
            instance_tab,
            instance_tab_bar,
            instance_carousel,
    ):
        # Removes a tab by clicking on the close icon on the left.
        for instance_tab in instance_carousel.slides:
            if instance_tab.tab_label_text == instance_tab_label.text:
                instance_tabs.remove_widget(instance_tab_label)
                self.index -= 1
                break
# .split('-')[1]

    def on_text(self):
        text = self.screenMain.ids.lien.text
        if text:
            self.screenMain.ids.spinner.active = True
            asynckivy.start(self.start_source(text))
        else:
            self.screenMain.ids.spinner.active = False
    
    async def start_source(self, text):
        await asynckivy.sleep(0.2)
        start_video = CamCapture(text, self.screenMain)
        lancer = await start_video.lancer()
        if lancer:
            print(f"start_source====>>>> {lancer}")
        self.screenMain.ids.spinner.active = False


app = AppCameraLive()
app.run()

