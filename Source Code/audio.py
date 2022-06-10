import sounddevice as sd
import soundfile as sf
import time

from sqlalchemy import false

class Audio:
    def __init__(self):
        self.data = ''
        self.fs = 0
        
    def loadFile(self, path):
        self.data, self.fs = sf.read(path, dtype='float32')
        self.name = path.split('/')[-1]
        self.time = self.data.shape[0] // self.fs

    def palyAndRec(self):
        self.myRecord = sd.playrec(self.data, self.fs, channels=2)
        self.save = True
    
    def stopAudio(self):
        sd.stop()
        self.save = False
    
    def saveFile(self, save_path):
        self.save_path = save_path + '/' + self.name.replace('.','_1.')
        if(self.save):
            sf.write(self.save_path, self.myRecord, self.fs)



