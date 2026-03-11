import customtkinter as ctk
from typing import TypedDict
from src.app_config import AppConfig
from src.widget import Widget
from src.controller.controller import Controller

class FrameBase(ctk.CTkFrame, Widget):
    def __init__(self, master, app_config: AppConfig, controller: Controller, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, *args, **kwargs)
        Widget.__init__(self, app_config, controller)
        self.fonts = (self.app_config.font_name, 15)
        self.setup()
    def setup(self):
        pass