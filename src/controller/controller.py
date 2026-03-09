from src.data.app_data import AppData

class Controller:
    def __init__(self):
        self.data = AppData()

    # index, name
    def set_current_device(self, device: tuple[int, str]):
        self.data.current_device = device

    def get_current_device(self) -> tuple[int, str]:
        return self.data.current_device
    
    def has_device(self) -> bool:
        return self.data.current_device is not None