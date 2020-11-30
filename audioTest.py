from cmu_112_graphics import *
import audioDriver
import time
    


class audioTest(App):
    def appStarted(app):
        app.timerDelay = 1
        #app.driver = audioDriver.audioDriver("all")
        app.beatCount = 0
    
    def timerFired(app):
        print(app.beatCount)
    
    def beat(app, beat, subdivision):
        app.beatCount = beat

    def playSound(app, name): #Do i need a musicThread? or can I universalize a thread type
        thread = audioDriver.audioThread(1, "soundThread", name)
        thread.start() 

    def keyPressed(app, event):
        if event.key == "Space":
            thread = audioDriver.musicThread(app, "soundThread", "VivaLaVida.wav")
            thread.start()
            #app.driver.playTrack(app, "VivaLaVida.wav")
            #playSound(app, "HitLongLeft1.wav")

    def redrawAll(app, canvas):
        return
        canvas.create_text(20,20,font="Arial 20 bold", 
            text=f"timerDelay: {app.timerDelay}", anchor = "nw")
        canvas.create_text(20,100,font="Arial 20 bold", 
            text=f"FrameSize: {app.frameChunk}", anchor = "nw")

    def closeApp(app):
        return

def almostEquals(a,b):
    epsilon = 10**-4
    if abs(a-b) < epsilon:
        return True



audioTest(width=400, height=500)