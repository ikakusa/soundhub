import customtkinter as ctk
from typing import TypedDict
from src.app_config import AppConfig
from src.main_app import MainApp
from src.controller.controller import Controller

app_config = AppConfig()
controller = Controller(app_config)

if __name__ == "__main__":
    app = MainApp(app_config, controller)
    app.mainloop()