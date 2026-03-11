from src.data.app_data import AppData
from src.logger.logger import Logger
from src.app_config import AppConfig
import sounddevice as sd
import threading
import time
import numpy as np
import librosa
import pyrubberband as rb

class Controller:
    def __init__(self, app_config: AppConfig):
        self.mic_phase = 0
        self.data = AppData()
        self.app_config = app_config
        threading.Thread(target=self.refresh_device_list, daemon=True).start()

    def set_pitch(self, v: float):
        self.data.pitch = v

    def set_gain(self, v: float):
        self.data.gain = v

    def is_playing(self) -> bool:
        return self.data.playing_custom
    
    def set_change_gain(self, state: bool):
        self.data.change_gain = state

    def set_change_pitch(self, state: bool):
        self.data.change_pitch = state

    def set_pipe_io(self, state: bool):
        self.data.pipe_io = state

    @staticmethod
    def scale(x):
        return 1 + 99 * (np.exp((x-1)/24) - 1) / (np.e - 1)

    @staticmethod
    def is_true(state: str):
        return state == "on"
    
    def toggle_play(self):
        if self.get_current_device(True)[0] == -1 or (self.get_current_device() == -1 and self.get_current_device() == -1):
            self.set_playing(False)
            return
        self.set_playing(not self.is_playing())

        if self.is_playing():
            self.start_mic_stream()
        else:
            if self.data.stream:
                self.data.stream.stop()
                self.data.stream.close()

    def set_playing(self, state: bool):
        self.data.playing_custom = state
    # index, name input = 0 output = 1
    def set_current_device(self, device: str, output_device = False):
        split = device.split(", ")
        index = split[0]
        device_name = split[1]
        self.data.current_devices[output_device] = (int(index), device_name)
        Logger.log(self.data.current_devices)

    # index, name
    def get_current_device(self, output_device = False) -> tuple[int, str]:
        return self.data.current_devices[output_device]
    
    def has_device(self) -> bool:
        return len(self.data.current_devices) > 1
    
    def refresh_device_list(self):
        while True:
            temp = [[], [], []]
            hostapi = sd.query_hostapis()
            for index, data in enumerate(sd.query_devices()):
                hostapi_name = hostapi[data["hostapi"]]["name"]
                if hostapi_name != "Windows WASAPI":
                    continue
                if data["max_input_channels"] > 0:
                    temp[0].append((index, data))
                if data["max_output_channels"] > 0:
                    temp[1].append((index, data))
                temp[2].append((index, data))
            self.data.device_list = temp.copy()
            time.sleep(0.1)

    def mic_callback(self, indata: np.ndarray, outdata: np.ndarray, frames: int, time, status):
        if not self.is_playing():
            outdata[:] = 0
            return
        gain = self.data.gain if self.data.change_gain else 1
        chunk = indata[:,0]
        shift = rb.pitch_shift(chunk, self.data.sample_rate, self.data.pitch) if self.data.change_pitch else chunk
        
        self.mic_phase += len(shift)
        if self.data.pipe_io:
            outdata[:,0] = np.clip(shift * (Controller.scale(gain)), -1, 1)
        else:
            outdata[:,0] = 0

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
