from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from studio.constants.GetNetworks import GetNetworks


class NotificationService:
    dialogConnectLiveBox = None
    dialogAddCamBox = None


    def start_connect_live(self):
        if not self.dialogConnectLiveBox:
            self.dialogConnectLiveBox = MDDialog(
                    title="[b][color=#5AA6FF]A propos[/color][/b]",
                    type="custom",
                    content_cls=ConnectLiveBox(),
                    md_bg_color="#262626",
            )
        self.dialogConnectLiveBox.open()    

    def add_cam_box(self):
        if not self.dialogAddCamBox:
            self.dialogAddCamBox = MDDialog(
                    title="[b][color=#5AA6FF]Ajouter un nouveau cam vidéo[/color][/b]",
                    type="custom",
                    content_cls=AddCamBox(),
                    md_bg_color="#262626",
            )
        self.dialogAddCamBox.open()


class ConnectLiveBox(MDBoxLayout):
    
     def demarrer(self):
        if self.ids.demarrer.text == "Démarrer":
            self.ids.demarrer.text = "Allumer"
            self.ids.demarrer.md_bg_color = '#00FF40'
            # print(self.app.screenMain.ids)
            # self.app.screenMain.ids.connect.ids.Camlive.ids.bage_card.md_bg_color = '#00FF40'
            self.app.demarer_connect_live_box()
        else:
            self.ids.demarrer.text = "Démarrer"
            self.ids.demarrer.md_bg_color = '#676767'
            self.app.stop_connect_live_box()


class AddCamBox(MDBoxLayout):
    menu_items_camera = None
    dropdown2 = None
    getnetworks = GetNetworks()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index["interface"]),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(items=self.menu_items_camera, width_mult=3, caller=self.ids.list_camera)

    
    def add_cam(self):
        # if self.ids.demarrer.text == "Démarrer":
        #     self.ids.demarrer.text = "Allumer"
        #     self.ids.demarrer.md_bg_color = '#00FF40'
        #     self.app.demarer_connect_live_box()
        # else:
        #     self.ids.demarrer.text = "Démarrer"
        #     self.ids.demarrer.md_bg_color = '#676767'
        #     self.app.stop_connect_live_box()
        pass
    
    def affiche_camera(self):

        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index["interface"]),
                "trailing_icon": str(index["trailing_icon"]),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_camera, width_mult=3, caller=self.ids.list_camera)

    def listcamera(self):
        self.dropdown2.open()
    
    def selectDropdownNetwork(self, text):
        ip = text["ip_address"]
        if ip == 0:
            self.ids.lien.text = str(f"{ip}")
        else:
            self.ids.lien.text = str(f"https:/{ip}")
        self.ids.lien.on_focus = True
        if self.dropdown2:
            self.dropdown2.dismiss()
