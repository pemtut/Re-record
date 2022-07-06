from regex import E
import sounddevice as sd
import soundfile as sf
import time
import logging

class Audio:
    def __init__(self):
        self.data = ''
        self.fs = 0
        
    def loadFile(self, path):
        try:
            self.data, self.fs = sf.read(path, dtype='float32')
            self.name = path.split('/')[-1]
            self.time = self.data.shape[0] // self.fs
            logging.debug(f'self.data = {self.data.shape} self.fs = {self.fs} self.name = {self.name} self.time = {self.time}')
            logging.info('Select files successfully')
        except Exception as e:
            logging.error(f'Error in load file. Error message: {e}')

    def palyAndRec(self):
        try:
            self.myRecord = sd.playrec(self.data, self.fs, channels=2)
            self.save = True
        except Exception as e:
            logging.error(f'Error in play and record. Error message: {e}')
    
    def stopAudio(self):
        try:
            sd.stop()
            self.save = False
            logging.debug('Stop in sounddevice function active correctly')
        except Exception as e:
            logging.error(f'Error in stop playing audio. Error message: {e}')

    def saveFile(self, save_path, rate, format):
        self.save_path = save_path + '/' + self.name.replace('.wav',f'_new.{format}')
        if(self.save):
            try:
                if(format == 'RAW'):
                    subtype = 'PCM_16'
                else:
                    subtype = sf.default_subtype(format)
                if(rate == 'default'):
                    sf.write(self.save_path, self.myRecord, self.fs, subtype=subtype, format=format)
                    logging.debug(f'Save file to {self.save_path} with sample rate = {self.fs} and format = {format}')
                else:
                    sf.write(self.save_path, self.myRecord, int(rate), subtype=subtype, format=format)
                    logging.debug(f'Save file to {self.save_path} with sample rate = {rate} and format = {format}')
            except Exception as e:
                logging.error(f'Error in save file. Error message: {e}')
    
    
    def setSavePath(self, save_path, format=None):
        if(format):
            self.save_path = save_path + '/' + self.name.replace('.','_1.')
        else:
            self.save_path = save_path + '/' + self.name.replace('.','_1.')



