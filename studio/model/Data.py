from studio.Service.DBCamlive import DatabaseManager
from studio.Service.NotificationService import NotificationService
from studio.controller.CamController import CamController
from studio.model.ThreadClass import ThreadManager
from studio.controller.ExpansionPanel import ExpansionPanelVid, FocusButton, IconButtonAction



class Data:
    index = 1
    listProces = []
    listCam = []
    connectLiveController = None
    menu_items_format = []
    menu_items_camera = []
    resource_cam_thread = None
    manager = ThreadManager()
    expansion = ExpansionPanelVid()
    expand_two = False
    expand_one = False

    def __init__(self, app) -> None:
        self.camController = CamController()
        self.camController.app = app
        self.db_manager = DatabaseManager("camlive.db")
