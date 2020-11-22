#SOUNDS FROM: https://www.youtube.com/watch?v=_bjZ_-VZVnU
#ORIGINAL BEAT SABER SOUNDS
#pyAudio basics: https://people.csail.mit.edu/hubert/pyaudio/docs/#:~:text=To%20use%20PyAudio%2C%20first%20instantiate,PyAudio.
import pyaudio
import wave
import sys
import time
import threading
import os

CHUNK = 1024

#p = pyaudio.PyAudio()

hitSounds = os.listdir("hitSounds")

class audioDriver(object):
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.sounds = dict()
        for fileName in hitSounds:
            self.sounds[fileName] = wave.open("hitSounds/" + fileName, 'rb')  

        wf = self.sounds[hitSounds[0]]
        self.stream = self.p.open(format=self.p.get_format_from_width(
                wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
            
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
    def playSound(self, name):
        wf = self.sounds[name]

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        # open stream using callback (3)
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        # start the stream (4)
        stream.start_stream()

        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.1)
        
        stream.stop_stream()
        stream.close()
        wf.close()

#THREADING TUTORIAL: https://www.tutorialspoint.com/python/python_multithreading.htm
class audioThread(threading.Thread):
   def __init__(self, threadID, name, soundName):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.soundName = soundName
      self.driver = audioDriver()

   def run(self):
      self.driver.playSound(self.soundName)

def testDriver():
    driver = audioDriver()
    driver.playSound("HitLongLeft1")
    driver.playSound("HitLongLeft2")

#testDriver()