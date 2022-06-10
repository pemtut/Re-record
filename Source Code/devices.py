import sounddevice as sd
import soundfile as sf
import pandas as pd
import numpy as np

class Devices:
    def __init__(self):
        self.devices = pd.DataFrame(sd.query_devices())
        self.available_devices = self.devices[self.devices['hostapi'] == 0]

        self.available_input_devices = self.available_devices[self.available_devices['max_output_channels'] == 0]
        self.available_output_devices = self.available_devices[self.available_devices['max_input_channels'] == 0]

        self.selected_input_index = sd.default.device[0]
        self.selected_output_index = sd.default.device[1]

    def changeInputDevices(self, idx):
        self.selected_input_index = idx
        sd.default.device[0] = idx

    def changeOutputDevices(self, idx):
        self.selected_output_index = idx
        sd.default.device[1] = idx

    def refreshSetting(self):
        sd._terminate()
        sd._initialize()
        self.__init__()


    