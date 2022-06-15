import sounddevice as sd
import soundfile as sf
import pandas as pd
import numpy as np
import logging

class Devices:
    def __init__(self):
        self.devices = pd.DataFrame(sd.query_devices())
        self.available_devices = self.devices[self.devices['hostapi'] == 0]

        self.available_input_devices = self.available_devices[self.available_devices['max_output_channels'] == 0]
        self.available_output_devices = self.available_devices[self.available_devices['max_input_channels'] == 0]

        self.selected_input_index = sd.default.device[0]
        self.selected_output_index = sd.default.device[1]
        
        pd.set_option('display.max_columns', None)
        logging.debug(f'Initiate device ...\n devices: {self.devices.loc[:,["name", "hostapi", "max_input_channels", "max_output_channels"]]} \n available_devices: {self.available_devices.loc[:,["name", "hostapi", "max_input_channels", "max_output_channels"]]} \n default device :{sd.default.device}')
    def changeInputDevices(self, idx):
        self.selected_input_index = idx
        sd.default.device[0] = idx
        logging.debug(f'Change input device to {idx}, Result {sd.default.device}')
        

    def changeOutputDevices(self, idx):
        self.selected_output_index = idx
        sd.default.device[1] = idx
        logging.debug(f'Change output device to {idx}, Result {sd.default.device}')

    def refreshSetting(self):
        try:
            sd._terminate()
            sd._initialize()
            self.__init__()
        except Exception as e:
            logging.error(f'Error in refresh. Error message {e}')


    