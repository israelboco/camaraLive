from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivymd.utils import asynckivy
from studio.controller.CamController import CamController
from studio.controller.ExpansionPanel import FocusButton
from studio.enum.FormatEnum import FormatEnum
from studio.view.CamCapture import CamCapture
from kivymd.toast import toast
from threading import Thread

from studio.view.CamViewImage import CamViewImage


class CardScrollImage(MDCard, CamViewImage):
    '''Class implementing content for a tab.''' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def on_start_video(self):
        asynckivy.start(self.on_start_video())
