import os
from datetime import datetime

import PIL
import cv2
from PIL import Image, ImageTk
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivymd.font_definitions import fonts
from kivymd.uix.screen import MDScreen
from kivymd.utils import asynckivy

from studio.view.CamCapture import CamCapture
# from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
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
        tab = Tab(title="CamLive-1")
        self.root.ids.tabs.add_widget(tab)
        camlive = CamCapture()
        process = MyProcess(target_function=camlive, args=())
        self.listProces.append(process)
        process.start()
        process.join()

    def on_stop(self):
        print(self.listProces)
        for proces in self.listProces:
            proces.terminate()
        print(self.listProces)

    def add_tab(self):
        self.index += 1
        name_tab = f"CamLive-{self.index}"
        self.root.ids.tabs.add_widget(
            Tab(
                id=str(self.index),
                tab_label_text=f"[ref={name_tab}][font={fonts[-1]['fn_regular']}]{md_icons['close']}[/font][/ref]{name_tab}"
            )
        )
        camlive = CamCapture()
        process = MyProcess(target_function=camlive, args=())
        self.listProces.append(process)
        process.start()
        process.join()

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
                index = int(instance_tab.id) - 1
                self.listProces[index].terminate()
                print(self.listProces[index])
                self.listProces.remove(self.listProces[index])
                print(self.listProces)
                # process.terminate()
                break
# .split('-')[1]


app = AppCameraLive()
app.run()

