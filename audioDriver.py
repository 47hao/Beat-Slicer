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

class AudioDriver(object):

    def __init__(self):
        print('got to this')
        self.p = pyaudio.PyAudio()
        self.sounds = dict() #upload all sounds
        for fileName in hitSounds:
            self.sounds[fileName] = wave.open("hitSounds/" + fileName, 'rb')  
        self.currentFrames = None
        self.wavPositions = []
        self.playingFiles = []

        wf = self.sounds[hitSounds[0]]
        print('reached here')
        self.stream = self.p.open(format=self.p.get_format_from_width(
                wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=self.callback)
        print('here, too')
        
        self.running = True
        #self.runStream()
        
    def runStream(self):
        thread = audioThread(1, "thread-1", self)
        #self.stream.start_stream
        thread.start()
        '''
        while(self.running):
            #time.sleep(0.1)
            print('wait')
        '''
    def checkStreamActive(self):
        return self.stream.is_active()

    def callback(self, in_data, frame_count, time_info, status):
        #print('im right here')
        for i in range(len(self.playingFiles)):
            #print('hmph')
            wavPos = self.wavPositions[i]
            playFile = self.playingFiles[i]
            wf = self.sounds[playFile]
            data = wf.readframes(frame_count)
            #print(data)
            self.wavPositions[i] += frame_count
            return (data, pyaudio.paContinue)
            #print('ok')
        return (None, pyaudio.paContinue)

    def close(self):
        print("CLOSING STREAM")
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
    def playSound(self, name):
        wf = self.sounds[hitSounds[0]]
        stream = self.p.open(format=self.p.get_format_from_width(
                wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=self.callback)

        print("stream active:", self.stream.is_active())
        self.playingFiles.append(name)
        self.wavPositions.append(0)
        stream.start_stream()
        #print(len(self.playingFiles))
        #wf = self.sounds[name]

        # wait for stream to finish (5)

#THREADING TUTORIAL: https://www.tutorialspoint.com/python/python_multithreading.htm

class audioThread(threading.Thread):
    def __init__(self, threadID, name, audioDriver):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.driver = audioDriver
        #self.driver.stream.start_stream()

    def run(self):
        self.driver.stream.start_stream()
        while(self.driver.running): #continues to tick when game ends...
            #time.sleep(0.1)
            print(self.driver.running)
        #self.driver.playSound(self.soundName)


class Test(object):
    def __init__(self):
        self.driver = AudioDriver()
    
    def playSound(self, name):
        self.driver.playSound(name)
    

def testDriver():
    testObj = Test()
    testObj.playSound("HitShortLeft5.wav")
    '''
    driver = audioDriver()
    driver.playSound("HitLongLeft1.wav")
    driver.playSound("HitLongLeft2.wav")
    '''
testDriver()