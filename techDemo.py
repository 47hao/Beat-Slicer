from cmu_112_graphics import *

import camTracker
import audioDriver
#import audioThread
import threading

class Game(App):
    def appStarted(app):
        app.debugMode = True
        app.maxThreads = 4
        app.runThreads = False
        
        app.timerDelay = 5
        app.camThreshold = .9
        app.cam = camTracker.camTracker()

        app.xPos = 0
        app.yPos = 0

        app.audioDriver = audioDriver.audioDriver()
    
    def keyPressed(app, event):
        #controlling camera sensitivity
        if event.key == 'Up':
            if(app.camThreshold) < .95:
                app.camThreshold += .05
        elif event.key == 'Down':
            if(app.camThreshold) > .5:
                app.camThreshold -= .05
        elif event.key == 'Space':
            app.cam.toggleFilter()
        
        elif event.key == 's':
            app.playSound("HitShortLeft4.wav")
        elif event.key == 'd':
            app.playSound("HitShortLeft2.wav")

    def playSound(app, name):
        thread = audioDriver.audioThread(1, "soundThread", name)
        thread.start()

    def timerFired(app):
        if(app.runThreads):
            if(app.countCamThreads() < app.maxThreads):
                thread = camThread(2, "camThread", app)
                thread.start()
        else:
            app.camTick()
        print(app.countCamThreads())
        #print(threading.enumerate()[0])
    
    def countCamThreads(app):
        threads = threading.enumerate()
        count = 0
        for t in threads:
            if t.name == "camThread":
                count += 1
        return count

    def camTick(app):
        output = app.cam.getCoords(app.camThreshold)
        if(output != None):
            (xScale, yScale) = output
            app.xPos = app.width*(1-xScale) #camera's flipped
            app.yPos = app.height*yScale
    
    def redrawAll(app, canvas):
        if(app.debugMode):
            app.drawReferenceMarker(canvas)

    def drawReferenceMarker(app, canvas):
        r = 10
        canvas.create_oval(app.xPos-r, app.yPos-r, app.xPos+r, app.yPos+r,
                            fill = "red", outline = "")

    def closeApp(app):
        app.audioDriver.close()
sdsdss
#Threading Tutorial: from here
#https://www.tutorialspoint.com/python/python_multithreading.htm
class camThread(threading.Thread):
    def __init__(self, threadID, name, game):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game = game

    def run(self):
        self.game.camTick()

Game(width=900,height=600)