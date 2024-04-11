from kivy.properties import ObjectProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.''' 
    
    def on_text(self):
        text = self.ids.source.text
        if text:
            self.ids.spinner.active = True
            self.start_source(text)
        else:
            self.ids.spinner.active = False
    
    def start_source(self, text):
        pass
