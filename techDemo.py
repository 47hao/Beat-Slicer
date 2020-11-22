from cmu_112_graphics import *

import camTracker
import audioDriver
import threading

class Game(App):
    def appStarted(app):
        app.debugMode = True

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
            print("s'd")
            #thread.start_new_thread(app.audioDriver.playSound, ("HitLongLeft1"))
            app.audioDriver.playSound("HitLongLeft2")

    def timerFired(app):
        app.camTick()
    
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

Game(width=900,height=600)