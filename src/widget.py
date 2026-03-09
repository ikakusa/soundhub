from typing import TypedDict, TYPE_CHECKING
import customtkinter as ctk
from src.app_config import *
from src.controller.controller import Controller

if TYPE_CHECKING:
    from src.frames.frame_base import *

class ButtonHolder(TypedDict):
    id: ctk.CTkButton
class LabelHolder(TypedDict):
    id: ctk.CTkLabel
class FrameHolder(TypedDict):
    id: "FrameBase"

class ComboHolder(TypedDict):
    id: ctk.CTkComboBox

class Widget:
    #grid: (row, column) 
    def __init__(self, app_config: AppConfig, controller: Controller):
        self.controller = controller
        self.app_config = app_config
        self.buttons: ButtonHolder = {}
        self.labels: LabelHolder = {}
        self.frames: FrameHolder = {}
        self.combos: ComboHolder = {}

    #padding = (x, y)
    def add_button(self, id, padding, grid, button, sticky=None):
        self.buttons[id] = button
        button.grid(row=grid[0], column=grid[1], padx=padding[0], pady=padding[1], sticky=sticky)

    def add_label(self, id, grid, padding, label, sticky=None):
        self.labels[id] = label
        label.grid(row=grid[0], column=grid[1], padx=padding[0], pady=padding[1], sticky=sticky)

    def add_frame(self, id, grid, padding, frame, sticky=None):
        self.frames[id] = frame
        frame.grid(row=grid[0], column=grid[1], padx=padding[0], pady=padding[1], sticky=sticky)

    def add_combobox(self, id, grid, padding, combo, sticky=None):
        self.combos[id] = combo
        combo.grid(row=grid[0], column=grid[1], padx=padding[0], pady=padding[1], sticky=sticky)