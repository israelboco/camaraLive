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
from kivymd.uix.screen import MDScreen
from kivymd.utils import asynckivy

# from apscheduler.schedulers.blocking import BlockingScheduler as Scheduler
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from studio.view.CameraFrame import Camera
from studio.view.MenuFrame import MenuBar
from studio.view.ScreenMain import ScreenMain
from studio.view.Tabs import Tab
from kivymd.icon_definitions import md_icons

Builder.load_file("studio/view/kv/main.kv")


class AppCameraLive(MDApp):
    icons = list(md_icons.keys())[15:19]

    def build(self) -> MDScreen:
        self.title = "Camera Live"
        self.screenMain = ScreenMain()
        return self.screenMain

    def on_start(self):

        for name_tab in self.icons:
            tab = Tab(title="Cam " + name_tab)
            self.root.ids.tabs.add_widget(tab)


app = AppCameraLive()
app.run()

