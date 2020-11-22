#!/usr/bin/python

import threading
import time
import audioDriver

exitFlag = 0

#THREADING TUTORIAL: https://www.tutorialspoint.com/python/python_multithreading.htm
class audioThread(threading.Thread):
   def __init__(self, threadID, name, soundName):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.soundName = soundName
      self.driver = audioDriver.audioDriver()

   def run(self):
      self.driver.playSound(self.soundName)
'''
# Create new threads
thread1 = audioThread(1, "Thread-1", 1)
thread2 = audioThread(2, "Thread-2", 2)
thread3 = audioThread(2, "Thread-3", 2)
thread4 = audioThread(2, "Thread-4", 2)
# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
'''