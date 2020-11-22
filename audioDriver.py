#SOUNDS FROM: https://www.youtube.com/watch?v=_bjZ_-VZVnU
#ORIGINAL BEAT SABER SOUNDS
#pyAudio basics: https://people.csail.mit.edu/hubert/pyaudio/docs/#:~:text=To%20use%20PyAudio%2C%20first%20instantiate,PyAudio.
import pyaudio
import wave
import sys

CHUNK = 1024

#p = pyaudio.PyAudio()

hitSounds = ["HitLongLeft1","HitLongLeft2"]

class audioDriver(object):
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.sounds = dict()
        for fileName in hitSounds:
            self.sounds[fileName] = wave.open("hitSounds/" + fileName + ".wav", 'rb')  

        wf = self.sounds[hitSounds[0]]
        self.stream = self.p.open(format=self.p.get_format_from_width(
                wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
            
    def close(self):
        # stop stream (4)
        self.stream.stop_stream()
        self.stream.close()
        # close PyAudio (5)
        self.p.terminate()
    
    def playSound(self, name):
        wf = self.sounds[name]
        print(wf)
        # read data
        data = wf.readframes(CHUNK)
        # play stream (3)
        while len(data) > 0:
            self.stream.write(data)
            data = wf.readframes(CHUNK)

def testDriver():
    driver = audioDriver()
    driver.playSound("HitLongLeft1")
    driver.playSound("HitLongLeft2")