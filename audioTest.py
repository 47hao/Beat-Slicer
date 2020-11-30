from cmu_112_graphics import *
import audioDriver
import time

def appStarted(app):
    app.timerDelay = 25
    app.ticks = 0
    app.frameChunk = 512
    app.driver = audioDriver.audioDriver(True)
    app.driver.playTrack("VivaLaVida.wav")
    
'''
def timerFired(app):
    app.ticks += 1
    app.driver.stepMusic(app.frameChunk)
    
    trueTime = app.lastTime - time.time()
    print("time:", trueTime)
    #app.frameChunk = trueTime * 20
    app.lastTime = time.time()
'''
def playSound(app, name):
    thread = audioDriver.audioThread(1, "soundThread", name)
    thread.start()

def keyPressed(app, event):
    if event.key == "Up":
        app.timerDelay += 1
    elif event.key == "Down":
        app.timerDelay -= 1
    elif event.key == "Left":
        app.frameChunk //= 2
    elif event.key == "Right":
        app.frameChunk *= 2
    elif event.key == "Space":
        playSound(app, "HitLongLeft1.wav")

def redrawAll(app, canvas):
    canvas.create_text(20,20,font="Arial 20 bold", 
        text=f"timerDelay: {app.timerDelay}", anchor = "nw")
    canvas.create_text(20,100,font="Arial 20 bold", 
        text=f"FrameSize: {app.frameChunk}", anchor = "nw")

    #3ms delay = 256 frames
    #8ms delay = 512 frames
    #20ms delay = 1024

def closeApp(app):
    return

runApp(width =400, height=500)