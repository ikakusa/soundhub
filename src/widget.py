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

class Widget:
    def __init__(self, app_config: AppConfig, controller: Controller):
        self.controller = controller
        self.app_config = app_config
        self.buttons: ButtonHolder = {}
        self.labels: LabelHolder = {}
        self.frames: FrameHolder = {}

    def add_button(self, id, grid, button):
        self.buttons[id] = button
        button.grid(row=grid[0], column=grid[1])

    def add_label(self, id, grid, label):
        self.labels[id] = label
        label.grid(row=grid[0], column=grid[1])

    def add_frame(self, id, grid, padding, frame):
        self.frames[id] = frame
        frame.grid(row=grid[0], column=grid[1], padx=padding[0], pady=padding[1])