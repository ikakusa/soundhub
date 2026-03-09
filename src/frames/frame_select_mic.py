import customtkinter as ctk
from typing import TypedDict
from src.app_config import *
from src.frames.frame_base import *

class SelectMicFrame(FrameBase):
    def parse_device_text(self):
        return self.controller.get_current_device()[1] if self.controller.has_device() else "未選択"
    def setup(self):
        self.add_label("label.current_mic", (0, 0), ctk.CTkLabel(master=self, text=f"現在のマイク: {self.parse_device_text()}", font=self.fonts))