import customtkinter as ctk
from src.widget import Widget
from src.app_config import AppConfig
from src.frames.frame_custom_audio import CustomAudioFrame
from src.controller.controller import Controller

class MainApp(ctk.CTk, Widget):
    def __init__(self, app_config: AppConfig, controller: Controller):
        ctk.CTk.__init__(self)
        Widget.__init__(self, app_config, controller)

        self.resizable(False, False)
        self.geometry("1000x550")
        self.title("Sound Hub")
        self.grid_columnconfigure(0, weight=1)
        self.setup()

    def setup(self):
        ctk.set_appearance_mode(self.app_config.appearance_mode)
        ctk.set_default_color_theme(self.app_config.color_theme)
        
        self.add_frame(id="frame.select_mic", grid=(0, 0), sticky="we", padding=(20, 20), frame=CustomAudioFrame(self, self.app_config, self.controller))