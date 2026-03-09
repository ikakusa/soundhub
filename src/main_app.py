import customtkinter as ctk
from src.widget import Widget
from src.app_config import AppConfig
from src.frames.frame_select_mic import SelectMicFrame
from src.controller.controller import Controller

class MainApp(ctk.CTk, Widget):
    def __init__(self, app_config: AppConfig, controller: Controller):
        ctk.CTk.__init__(self)
        Widget.__init__(self, app_config, controller)

        self.resizable(False, False)
        self.geometry("1000x550")
        self.title("Sound Hub")
        self.setup()

    def setup(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.add_frame("frame.select_mic", (0, 0), (20, 20), SelectMicFrame(self, self.app_config, self.controller))