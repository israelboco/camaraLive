import kivymd  
from kivy.lang import Builder
from kivymd.app import MDApp 
from kivymd.font_definitions import fonts
from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
from kivymd.utils import asynckivy 
from kivymd.toast import toast
from threading import Thread
from studio.Service.NotificationService import NotificationService
from studio.constants.GetNetworks import GetNetworks
from studio.controller.ConnectLiveController import ConnectLiveController
from studio.controller.CamController import  CamController
from studio.enum.FormatEnum import FormatEnum
from studio.model.Data import Data
from studio.view import CamViewImage
from studio.controller.ExpansionPanel import FocusButton, IconButtonAction
from studio.view.CamCapture import CamCapture
from studio.view.CameraFrame import Camera
from studio.view.CardAudio import CardAudio
from studio.view.MyProcess import MyProcess
from studio.view.ScreenMain import MainScreenView,  ScreenMain
from kivymd.icon_definitions import md_icons

from studio.view.TabVideos import CardScrollImage


class AppCameraLive(MDApp):
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.dropdown = MDDropdownMenu()
        self.main_view = MainScreenView()
        self.getnetworks = GetNetworks()
        self.notificationService = NotificationService()
        self.screenMain = self.main_view.screen_main
        self.data = Data(self)

    def build(self) -> MDScreen:
        self.title = "Cam Live"
        self.icon = "studio/asset/Logo.ico"
        return self.main_view

    def on_start(self):
        self.affiche_format()
        self.affiche_camera()
        self.affiche_audio()
        self.data.expansion.start_expand_one() 
        self.data.expansion.start_expand_two()
        self.data.db_manager.create_table()
    
    def start_card_view(self):
        if self.data.expand_two:
            self.screenMain.ids.two_widget.add_widget(self.data.expansion.expand_two)
            self.data.expand_two = False
        else:
            self.screenMain.ids.two_widget.remove_widget(self.data.expansion.expand_two)
            self.data.expand_two = True

    def start_connexion(self):
        if self.data.expand_one:
            self.screenMain.ids.one_widget.add_widget(self.data.expansion.expand_one)
            self.data.expand_one = False
        else:
            self.screenMain.ids.one_widget.remove_widget(self.data.expansion.expand_one)
            self.data.expand_one = True
    
    def open_param(self):
        self.notificationService.open_param()

    def on_stop(self):
        print("Arrêt du programme principal...")
        self.data.manager.stop_all_threads()
        self.data.db_manager.close_connection()

    def add_tab(self, text):
        try:
            print('top')
            self.data.index += 1
            tab = CardScrollImage(
                text, self
                )
            self.screenMain.ids.box_video.add_widget(tab) 
        except Exception as e:
            print(e)
        self.affiche_audio()

    def remove_tab(self):
        if self.data.index > 1:
            self.data.index -= 1
        self.screenMain.ids.box_video.remove_widget(
            self.screenMain.ids.box_video.get_tab_list()[-1]
        )

    def on_ref_press(
            self,
            instance_tab_videos,
            instance_tab_label,
            instance_tab,
            instance_tab_bar,
            instance_carousel,
    ):
        for instance_tab in instance_carousel.slides:
            if instance_tab.tab_label_text == instance_tab_label.text:
                instance_tab_videos.remove_widget(instance_tab_label)
                self.index -= 1
                break 

    async def on_start_video(self):
        self.screenMain.ids.spinner.active = True
        await asynckivy.sleep(2)
        if self.data.camController.videoCamera:
            self.screenMain.ids.spinner.active = False
            return toast("stopper d'abord la camera en cours.")
        self.resource_cam_thread = None
        await self.async_cam_thread()
        self.screenMain.ids.spinner.active = False
    
    async def async_cam_thread(self):
        text = self.screenMain.ids.lien.text
        if text:
            asynckivy.start(self.start_source(text))
    
    async def start_source(self, text):
        cam = None
        for content in self.data.listCam:
            listText= content[0]
            if text == listText:
                cam = content[1]
                break
        lancer = await self.data.camController.add_start_video(text, self.screenMain, cam)
        if not lancer:
            return
        if not self.data.connectLiveController:
            print("===============>>>>>>> connectLiveController")
            self.data.connectLiveController = ConnectLiveController(self.data.camController)
        if lancer:
            print(f"start_source====>>>> {lancer}")
            if not cam:
                self.data.listCam.append((text, lancer))

    def affiche_format(self):
       
        self.menu_items_format = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index.name),
                "on_release": lambda x=index: self.selectDropdown(x),
            } for index in list(FormatEnum)
        ]

        self.dropdown1 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_format, width_mult=3, caller=self.screenMain.ids.shape)

    def listDropdown(self):
        self.dropdown1.open()

    def affiche_camera(self):

        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index["interface"]),
                "trailing_icon": str(index["trailing_icon"]),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_camera, width_mult=3, caller=self.screenMain.ids.list_camera)


    def affiche_audio(self):

        self.menu_items_audio = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Audio Cam {str(index + 1)}",
                "on_release": lambda x=f"Audio Cam {str(index + 1)}": self.selectDropdownAudio(x),
            } for index in range(0, self.data.index)
        ]

        self.dropdown3 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_audio, width_mult=3, caller=self.screenMain.ids.microphone)

    def listaudio(self):
        self.dropdown3.open()

    def listcamera(self):
        self.dropdown2.open()


    def selectDropdown(self, text):
        self.screenMain.ids.label_format.text = "[color=#4287f5]format :" + str(text.value) + "[/color]"
        self.data.camController.select_format(text.value)
        if self.dropdown1:
            self.dropdown1.dismiss()
    
    def selectDropdownNetwork(self, text):
        ip = text["ip_address"]
        if ip == 0:
            self.screenMain.ids.lien.text = str(f"{ip}")
        else:
            self.screenMain.ids.lien.text = str(f"https:/{ip}")
            self.screenMain.ids.lien.focus = True
        if self.dropdown2:
            self.dropdown2.dismiss()
    
    def selectDropdownAudio(self, text):
        self.screenMain.ids.audio.text = str("[color=#4287f5]" + text + "[/color]")
        # self.camController.start_source(text)
        if self.dropdown3:
            self.dropdown3.dismiss()
     
    def start_connect_live(self):
        if not self.data.camController.videoCamera:
            return toast("connectez vous a un camera")
        self.notificationService.start_connect_live()
    
    def demarer_connect_live_box(self):
        self.data.connectLiveController.start()
    
    def stop_connect_live_box(self):
        self.data.connectLiveController.stop()

app = AppCameraLive()
app.run()