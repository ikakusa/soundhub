import customtkinter as ctk
from typing import TypedDict
from src.app_config import *
from src.frames.frame_base import *
import threading
import time

class CustomAudioFrame(FrameBase):
    def parse_device_text(self, output_device = False):
        return self.controller.get_current_device(output_device)[1] if self.controller.get_current_device(output_device)[0] != -1 else "未選択"
    def update_current_mic_label(self):
        self.labels["label.current_mic_i_value"].configure(text=self.parse_device_text(False))
        self.labels["label.current_mic_o_value"].configure(text=self.parse_device_text(True))
        self.after(500, self.update_current_mic_label)
    def setup(self):

        self.add_label(id="label.current_mic_i", grid=(0, 0), padding=(10, 0), sticky="w", label=ctk.CTkLabel(master=self, text="現在の入力マイク: ", font=self.app_config.fonts))
        self.add_label(id="label.current_mic_i_value", grid=(0, 1), padding=(0, 0), sticky="w", label=ctk.CTkLabel(master=self, text=self.parse_device_text(False), font=self.app_config.fonts))
        
        self.add_label(id="label.current_mic_o", grid=(1, 0), padding=(10, 0), sticky="w", label=ctk.CTkLabel(master=self, text=f"現在の出力マイク: ", font=self.app_config.fonts))
        self.add_label(id="label.current_mic_o_value", grid=(1, 1), padding=(0, 0), sticky="w", label=ctk.CTkLabel(master=self, text=self.parse_device_text(True), font=self.app_config.fonts))
        
        self.add_label(id="label.select_input", grid=(2, 0), padding=(10, 30), sticky="w", label=ctk.CTkLabel(master=self, width=170, anchor="w", text=f"入力マイクを選択", font=self.app_config.fonts))
        self.add_combobox(id="combo.device_list", sticky="w", grid=(2, 1), padding=(0, 0), combo=ctk.CTkComboBox(master=self, width=250, font=self.app_config.fonts, values=[f"{i}, {d['name']}" for i, d in self.controller.get_device_list()], command=lambda choice: self.controller.set_current_device(choice, False)))
        
        self.add_label(id="label.select_output", grid=(3, 0), padding=(10, 0), sticky="w", label=ctk.CTkLabel(master=self, width=170, anchor="w", text=f"出力マイクを選択", font=self.app_config.fonts))
        self.add_combobox(id="combo.device_list", sticky="w", grid=(3, 1), padding=(0, 0), combo=ctk.CTkComboBox(master=self, width=250, font=self.app_config.fonts, values=[f"{i}, {d['name']}" for i, d in self.controller.get_device_list()], command=lambda choice: self.controller.set_current_device(choice, True)))

        self.update_current_mic_label()