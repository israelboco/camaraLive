from studio.controller.CamController import CamController


class Data:
    index = 1
    listProces = []
    listCam = []
    camController = CamController()
    connectLiveController = None
    menu_items_format = []
    menu_items_camera = []
    resource_cam_thread = None