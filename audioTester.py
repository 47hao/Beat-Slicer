import audioDriver

class Test(object):
    def __init__(self):
        self.driver = audioDriver.AudioDriver()
    
    def playSound(self, name):
        self.driver.playSound(name)
    

def testDriver():
    testObj = Test()
    testObj.playSound("HitShortLeft5.wav")
    #while(True):
    #    testObj.playSound("HitLongLeft1.wav")
    #    testObj.playSound("HitShortRight1.wav")
    '''
    driver = audioDriver()
    driver.playSound("HitLongLeft1.wav")
    driver.playSound("HitLongLeft2.wav")
    '''
testDriver()