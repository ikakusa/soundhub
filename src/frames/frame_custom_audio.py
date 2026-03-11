import customtkinter as ctk
from typing import TypedDict
from src.app_config import *
from src.frames.frame_base import *
import threading
import time
import math
class CustomAudioFrame(FrameBase):
    def setup(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0, minsize=520)
        self.add_frame(id="frame.left_panel", grid=(0, 0), sticky="nw", padding=(10, 10), frame=CustomAudio_LeftPanel(master=self, app_config=self.app_config, controller=self.controller))
        self.add_frame(id="frame.right_panel", grid=(0, 1), sticky="nsew", padding=((0, 10), 10), frame=CustomAudio_RightPanel(master=self, app_config=self.app_config, controller=self.controller))

class CustomAudio_RightPanel(FrameBase):
    def update_elements(self):
        self.controller.set_pitch(self.sliders["slider.pitch"].get())
        self.controller.set_gain(self.sliders["slider.gain"].get())
        self.labels["label.pitch_slider"].configure(text=str(math.floor(self.controller.data.pitch*10) / 10))
        self.labels["label.gain_slider"].configure(text=str(math.floor(self.controller.data.gain*10) / 10))
        self.after(5, self.update_elements)
    def setup(self):
        pipe_io_v = ctk.StringVar(value="off")
        change_pitch_v = ctk.StringVar(value="off")
        change_gain_v = ctk.StringVar(value="off")

        pitch_slider = ctk.CTkSlider(master=self, from_=-20, to=20, number_of_steps=400)
        gain_slider = ctk.CTkSlider(master=self, from_=1, to=50, number_of_steps=49)
        gain_slider.set(1)
        
        self.add_checkbox("check.change_pitch", grid=(0, 0), padding=(10, 10), sticky="w", checkbox=ctk.CTkCheckBox(master=self, text="ピッチを変更する", checkbox_width=18, checkbox_height=18, variable=change_pitch_v, command=lambda : self.controller.set_change_pitch(Controller.is_true(change_pitch_v.get())), onvalue="on", offvalue="off", font=self.app_config.fonts))
        self.add_checkbox("check.change_gain", grid=(1, 0), padding=(10, 10), sticky="w", checkbox=ctk.CTkCheckBox(master=self, text="音量を変更する", checkbox_width=18, checkbox_height=18, variable=change_gain_v, command=lambda : self.controller.set_change_gain(Controller.is_true(change_gain_v.get())), onvalue="on", offvalue="off", font=self.app_config.fonts))
        self.add_checkbox("check.pipe_io", grid=(2, 0), padding=(10, 10), sticky="w", checkbox=ctk.CTkCheckBox(master=self, text="入力音声を別のデバイスに出力", checkbox_width=18, checkbox_height=18, variable=pipe_io_v, command=lambda : self.controller.set_pipe_io(Controller.is_true(pipe_io_v.get())), onvalue="on", offvalue="off", font=self.app_config.fonts))
        
        self.add_slider("slider.pitch", grid=(0, 1), padding=(10, 10), sticky="w", slider=pitch_slider)
        self.add_label("label.pitch_slider", grid=(0, 2), padding=(10, 10), sticky="w", label=ctk.CTkLabel(master=self, text=str(math.floor(self.controller.data.pitch*10) / 10)))
        
        self.add_slider("slider.gain", grid=(1, 1), padding=(10, 10), sticky="w", slider=gain_slider)
        self.add_label("label.gain_slider", grid=(1, 2), padding=(10, 10), sticky="w", label=ctk.CTkLabel(master=self, text=str(math.floor(self.controller.data.gain*10) / 10)))

        self.update_elements()
class CustomAudio_LeftPanel(FrameBase):
    def parse_device_text(self, output_device = False):
        return self.controller.get_current_device(output_device)[1] if self.controller.get_current_device(output_device)[0] != -1 else "未選択"
    def update_elements(self):
        self.labels["label.current_mic_i_value"].configure(text=self.parse_device_text(False))
        self.labels["label.current_mic_o_value"].configure(text=self.parse_device_text(True))

        self.buttons["button.start_stream"].configure(text="停止" if self.controller.is_playing() else "開始")
        self.after(10, self.update_elements)
    def setup(self):
        self.add_label(id="label.current_mic_i", grid=(0, 0), padding=(10, (10, 0)), sticky="w", label=ctk.CTkLabel(master=self, text="現在の入力マイク: ", font=self.app_config.fonts))
        self.add_label(id="label.current_mic_i_value", grid=(0, 1), padding=((0, 10), (10, 0)), sticky="w", label=ctk.CTkLabel(master=self, wraplength=self.app_config.wrap_length, text=self.parse_device_text(False), font=self.app_config.fonts))
        
        self.add_label(id="label.current_mic_o", grid=(1, 0), padding=(10, 0), sticky="w", label=ctk.CTkLabel(master=self, text=f"現在の出力マイク: ", font=self.app_config.fonts))
        self.add_label(id="label.current_mic_o_value", grid=(1, 1), padding=((0, 10), 0), sticky="w", label=ctk.CTkLabel(master=self, wraplength=self.app_config.wrap_length, text=self.parse_device_text(True), font=self.app_config.fonts))
        
        self.add_label(id="label.select_input", grid=(2, 0), padding=(10, (30, 5)), sticky="w", label=ctk.CTkLabel(master=self, anchor="w", text=f"入力マイクを選択", font=self.app_config.fonts))
        self.add_combobox(id="combo.device_list", sticky="w", grid=(2, 1), padding=((0, 10), (30, 5)), combo=ctk.CTkComboBox(master=self, width=250, font=self.app_config.fonts, values=[f"{i}, {d['name']}" for i, d in self.controller.get_device_list()[0]], command=lambda choice: self.controller.set_current_device(choice, False)))
        
        self.add_label(id="label.select_output", grid=(3, 0), padding=(10, 0), sticky="w", label=ctk.CTkLabel(master=self, width=80, anchor="w", text=f"出力マイクを選択", font=self.app_config.fonts))
        self.add_combobox(id="combo.device_list_2", sticky="w", grid=(3, 1), padding=((0, 10), 0), combo=ctk.CTkComboBox(master=self, width=250, font=self.app_config.fonts, values=[f"{i}, {d['name']}" for i, d in self.controller.get_device_list()[1]], command=lambda choice: self.controller.set_current_device(choice, True)))

        self.add_button(id="button.start_stream", grid=(4, 0), padding=(10, (20, 10)), sticky="w", button=ctk.CTkButton(master=self, text="停止" if self.controller.is_playing() else "開始", height=40, font=self.app_config.fonts, command=lambda: self.controller.toggle_play()))

        self.update_elements()