#SOUNDS FROM: https://www.youtube.com/watch?v=_bjZ_-VZVnU
#ORIGINAL BEAT SABER SOUNDS

#Viva La Vida track:
#https://www.youtube.com/watch?v=dvgZkm1xWPE


#pyAudio basics: https://people.csail.mit.edu/hubert/pyaudio/docs/#:~:text=To%20use%20PyAudio%2C%20first%20instantiate,PyAudio.
#synch concepts: https://www.gamasutra.com/blogs/YuChao/20170316/293814/Music_Syncing_in_Rhythm_Games.php
import pyaudio
import wave
import sys
import time
import threading
import os

#p = pyaudio.PyAudio()

hitSounds = os.listdir("hitSounds")
musics = os.listdir("music")
#(bpm, offset(ms))
bpm = {"VivaLaVida.wav":(138,1.7)}

class audioDriver(object):
    def __init__(self, soundDir):
        self.p = pyaudio.PyAudio()
        self.sounds = dict()
        self.currentBeat = None
        if soundDir == "all":
            print("LOADING ALL SOUND FILES...")
            for fileName in hitSounds:
                self.sounds[fileName] = wave.open("hitSounds/" + fileName, 'rb') 
            for fileName in musics:
                self.sounds[fileName] = wave.open("music/" + fileName, 'rb')
            self.sounds["tick"] = wave.open("music/" + fileName, 'rb') 
        else:
            name = soundDir.split("/")
            self.sounds[name[len(name)-1]] = wave.open(soundDir, 'rb')
    
    def playTrack(self, app, name):
        print("LOADING:", name)
        self.wf = self.sounds[name]
        frameRate = self.wf.getframerate()
        print("framerate:", frameRate)
        stream = self.p.open(format=self.p.get_format_from_width(
                self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=frameRate,
                output=True)
        
        #how many seconds long each beat is
        secondsPerBeat = 1/(bpm[name][0]/60)
        offset = bpm[name][1] #what units tho??

        subDivision = 1
        #duration of a quarter/sixteenth/whatever note
        secondsPerCount = secondsPerBeat/subDivision
        self.currentBeat = 0

        frameIndex = 0
        data = self.wf.readframes(1)
        while len(data) > 0 and app._running:
            stream.write(data)
            data = self.wf.readframes(1)
            frameIndex += 1
            seconds = frameIndex/frameRate #how many seconds in the song is
            if seconds/secondsPerBeat > self.currentBeat+offset:
                self.currentBeat += 1/subDivision
                self.playTick()
                app.beat(self.currentBeat, subDivision)
        
        #stop when done
        stream.stop_stream()
        stream.close()
    
    def playTick(self): #metronome clicks for testing
        thread = audioThread(1, "soundThread", "otherSounds/tick.wav")
        thread.start()

    def playSound(self, name):
        wf = self.sounds[name]

        def callback(in_data, frameCount, time_info, status):
            data = wf.readframes(frameCount)
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
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

#THREADING TUTORIAL: https://www.tutorialspoint.com/python/python_multithreading.htm
class audioThread(threading.Thread):
    def __init__(self, threadID, name, soundDir):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.soundDir = soundDir
        nameFrags = soundDir.split("/")
        self.soundName = nameFrags[len(nameFrags)-1]
        self.driver = audioDriver(soundDir)

    def run(self):
        self.driver.playSound(self.soundName)

class musicThread(threading.Thread):
    def __init__(self, app, threadID, name):
        threading.Thread.__init__(self)
        self.app = app
        self.threadID = threadID
        self.name = name
        self.driver = audioDriver("music/" + name)
    def run(self):
        self.driver.playTrack(self.app, self.name)

def testDriver():
    thread = audioThread(1, "soundThread", "hitSounds/HitShortLeft4.wav")
    thread.start()
    driver = audioDriver("all")
    driver.playTrack("VivaLaVida.wav")
    #driver.playSound("HitLongLeft1.wav")
    #driver.playSound("HitLongLeft2.wav")

#testDriver()