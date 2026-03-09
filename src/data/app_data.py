import sounddevice as sd
class AppData:
    def __init__(self):
        self.device_list: list[tuple[int, dict]] = []
        self.current_devices: list[tuple[int, str]] = [(-1, ""), (-1, "")]
        self.sample_rate = 48000
        self.channels = 1
        self.block_size = 8192 * 2
        self.gain = 1
        self.audio_path = ""
        self.playing_custom = False
        self.stream: sd.Stream = None
        self.pipe_i_o = False