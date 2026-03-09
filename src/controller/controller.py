from src.data.app_data import AppData
from src.logger.logger import Logger
from src.app_config import AppConfig
import sounddevice as sd
import threading
import time
import numpy as np

class Controller:
    def __init__(self, app_config: AppConfig):
        self.data = AppData()
        self.app_config = app_config
        threading.Thread(target=self.refresh_device_list, daemon=True).start()

    # index, name input = 0 output = 1
    def set_current_device(self, device: str, output_device = False):
        split = device.split(", ")
        index = split[0]
        device_name = split[1]
        self.data.current_devices[output_device] = (index, device_name)
        Logger.log(self.data.current_devices)

    # index, name
    def get_current_device(self, output_device = False) -> tuple[int, str]:
        return self.data.current_devices[output_device]
    
    def has_device(self) -> bool:
        return len(self.data.current_devices) > 1
    
    def refresh_device_list(self):
        while True:
            temp = []
            for index, data in enumerate(sd.query_devices()):
                if data["hostapi"] == 1:
                    temp.append((index, data))
            self.data.device_list = temp.copy()
            time.sleep(0.1)

    def mic_callback(self, indata: np.ndarray, outdata: np.ndarray, frames: int, time, status):
        if not self.data.playing_custom:
            return
        if self.data.pipe_i_o:
            outdata[:] = indata

    def start_mic_stream(self):
        input_device = self.get_current_device(False)[0]
        output_device = self.get_current_device(True)[0]

        if input_device == -1 and output_device != -1:
            input_device = output_device
        elif input_device != -1 and output_device == -1:
            return

        self.data.stream = sd.Stream(
            samplerate=self.data.sample_rate,
            blocksize=self.data.block_size,
            dtype=np.float32,
            channels=self.data.channels,
            callback=lambda indata, outdata, frames, time, status: self.mic_callback(indata, outdata, frames, time, status),
            device=(input_device, output_device)
        )
        self.data.stream.start()

    def get_device_list(self):
        return self.data.device_list
