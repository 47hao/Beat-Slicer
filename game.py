
from cmu_112_graphics import *
import grid3d
import slice3d
import poly3d
import cube
import beatCube
import blade
import math

#from maps import VivaLaVida
import songMaps

import audioDriver
import camTracker
import threading

#This project uses cmu_112_graphics, based on tkinter:
#https://www.cs.cmu.edu/~112/
#ModalApp from 112 animations part 3 notes

#Assets used in this project
#Music:
#Radioactive - Imagine Dragons (2012)
#Viva La Vida - Coldplay (2008)
#Seven Nation Army - The White Stripes(2003)
#Take on Me - Aha (1985)
#Sounds:
#Beat Saber (2018) Official sound effects
#Fonts: Orkney (Hanken Design Co.), Teko (Indian Type Foundry)

class Game(Mode):
    def appStarted(app):
        app.running = True
        app.debugMode = False
        app.maxThreads = 4
        app.runThreads = True

        app.focalLength = 600
        app.ticks = 0
        app.timerDelay = 1

        app.cubes = []
        app.polys = []
        app.cubeSpeed = 10 #no units

        app.grid = grid3d.Grid3d(app, app.focalLength)
        app.blade = blade.Blade(app)

        app.beatCount = 0
        #number of beats a block spawns beforehand
        app.preSpawnBeats = 6 #app.grid.startZ/app.cubeSpeed

        app.camThreshold = .9
        app.cam = camTracker.camTracker()
        app.playerPos = (0,0)

        cThread = camThread(1, "camThread", app)
        cThread.start()

        app.driver = audioDriver.audioDriver("all")

        app.totalScore = 0
        app.totalCubes = 0
        app.goodSlices = 0
        app.badSlices = 0

        app.sliceErrorRange = (0,0.5) #by how many beats the player can be off
        app.timeScoreWeight = 20
        app.sliceScoreWeight = 20

        app.songName = app.app.song
        app.loadSong()

        app.bgColor = (0,0,0)

    def loadSong(app):
        songInfo = songMaps.getMap(app.app.song)
        (bpm, delay, noteMap, fileName, songTitle, artist, startTime) = songInfo
        #pass info back to the game
        app.app.songTitle = songTitle
        app.app.artist = artist

        app.notes = dict()
        #contents = readFile("maps/" + app.songName + ".py")
        data = noteMap
        for note in data:
            beat = note.beat
            app.notes[beat] = app.notes.get(beat,[]) + [note]
        app.playMusic(songInfo)

    def timerFired(app):
        app.ticks += 1
        if app.ticks % 100 == 0:
            app.cleanCubes()

        app.backgroundTick()
        app.blade.bladeStep()
        app.moveCubes()
        app.bladeSlice()
        
        if(app.debugMode):
            app.cam.showFrame()
            print("DEBUG INFO ======")
            print(f"blade points: {len(app.blade.points)}")
            print(f"cubes: {len(app.cubes)}")
            print(f"polys: {len(app.polys)}")

    def countCamThreads(app):
        threads = threading.enumerate()
        count = 0
        for t in threads:
            if t.name == "camThread":
                count += 1
        return count
        
    def testPoly(app):
        testCube = cube.Cube((100,50,-20),(0,0,0),30)
        points = testCube.getPoints()
        points[3] = (0,-40,0)
        poly = poly3d.Poly3d((100,50,-20),(0,0,-2),points)
        app.polys.append(poly)

    def bladeSlice(app):
        for i in range(len(app.blade.points)-1):
            (x0,y0), (x1,y1) = app.blade.points[i][0], app.blade.points[i+1][0]
            #convert coords to 3-space and not screen space
            app.sliceAllCubes((x0-app.width/2,y0-app.height/2),
                                (x1-app.width/2,y1-app.height/2))

    def sliceAllCubes(app, p0, p1):
        (x0,y0),(x1,y1) = p0, p1
        plane = slice3d.pointsToPlane((x0,y0,0),(x1,y1,0),(0,0,-1*app.grid.focalLength/2))
        i = 0
        while i < len(app.cubes):
            cube = app.cubes[i]
            if cube.inSliceZone() and cube.lineInCube(p0, p1):
                #should always 
                (x0, y0),(x1, y1) = p0,p1
                result = app.sliceCube(cube, plane)
                success = result[0]
                #success = 
                if success and type(cube) == beatCube.BeatCube:
                    if cube.checkDir(p0, p1):
                        app.driver.playHitSound()
                        score = int(result[1])
                        app.totalScore += score
                        app.goodSlices += 1
                    else: #wrong direction
                        app.driver.playBadHitSound()
                        app.badSlices += 1
                else:
                    i += 1
                #move on; didn't slice
            else:
                i += 1
        app.cleanCubes()

    def sliceCube(app, cube, plane):
        polys = cube.sliceCube(plane)
        if polys == None:
            return False, None
        (poly1, poly2) = polys
        app.cubes.pop(app.cubes.index(cube))
        app.polys.extend([poly1,poly2])

        score = 0
        if(type(cube) == beatCube.BeatCube): #calculate score
            score = app.calculateScore(cube, poly1, poly2)

        return True, score
    
    def calculateScore(app, cube, poly1, poly2):
        #time score:
        timeDiff = abs(cube.targetBeat-app.beatCount)
        minError, maxError = app.sliceErrorRange
        errorPercent = min(timeDiff/(maxError-minError),1)#cap it at 1
        #^this value ranges from 0-1, with 0 being most accurate
        timeScore = (1-errorPercent)*app.timeScoreWeight
        #print("timeScores:", timeScore)

        #slice score:
        vol1, vol2 = poly1.volume, poly2.volume
        bigger = max(vol1, vol2)
        smaller = min(vol1,vol2)
        sizeRatio = 1-(bigger-smaller)/bigger #ranges 0-1, 0 best 1 worst
        sliceScore = sizeRatio**0.3*app.sliceScoreWeight #0.5 to 0 range
        #print("sliceScores:", sliceScore)
        baseScore = 100-app.sliceScoreWeight-app.timeScoreWeight
        totalScore = baseScore + sliceScore + timeScore
        return totalScore
        #give full score up to 1:2 ratio
   
    def addCubes(app, beat): #att beat 20, queue beat 24's cubes
        queueBeat = beat+app.preSpawnBeats
        if queueBeat in app.notes:
            for item in app.notes[queueBeat]:
                (xcol,yrow),direc = item.pos, item.direc
                (x,y) = app.grid.getLaneCoords(xcol, yrow)
                pos = (x,y,app.grid.startZ)
                vel = (0,0,-1*app.cubeSpeed)
                cubeParams = (pos, vel, app.grid.cubeSize)
                cube = beatCube.BeatCube(app.grid,cubeParams,direc,
                        queueBeat, app.preSpawnBeats)
                app.cubes.append(cube)
                app.totalCubes += 1
            
    def moveCubes(app):
        beat = app.beatCount
        for cube in app.cubes:
            pass
            #cube.updatePos(app.grid, beat)
            #cube.move(app.timerDelay)
        for poly in app.polys:
            poly.move(app.timerDelay)

    def cleanCubes(app):
        i = 0
        while i < len(app.cubes):
            cube = app.cubes[i]
            if cube.pos[2] < -1*app.focalLength-cube.sideLength:
                app.cubes.pop(i)
                #print(len(app.cubes))
            else: #frontmost cubes are lowest indices 
                break
        while i < len(app.polys):
            poly = app.polys[i]
            if (poly.pos[2] < -1*app.focalLength or abs(poly.pos[1]) > app.height or
                abs(poly.pos[0]) > app.width):
                app.polys.pop(i)
                #print(len(app.cubes))
            else: #frontmost cubes are lowest indices 
                return

    def playMusic(app, info):
        thread = audioDriver.musicThread(app.app, "soundThread", info)
        thread.start()
    
    def beat(app, beat, subdivision):
        app.beatCount = beat
        if almostEquals(beat, int(beat)):
            pass
            print(beat)
        for cube in app.cubes:
            cube.updatePos(app.grid, beat)
        app.addCubes(beat)
            
    def playSound(app, name): #Do i need a musicThread? or can I universalize a thread type
        thread = audioDriver.audioThread(1, "soundThread", name)
        thread.start() 

    def redrawAll(app, canvas):
        app.drawBackground(canvas)
        app.drawScore(canvas)
        #app.drawGrid(canvas)
        #canvas.create_rectangle(10,10,10+app.grid.cubeSize,10+app.grid.cubeSize)
        app.drawPolys(canvas)
        app.drawCubes(canvas)
        #app.drawSlice(canvas)
        app.blade.draw(canvas)
        if(app.debugMode):
            app.drawReferenceMarker(canvas)

    def drawReferenceMarker(app, canvas):
        r = 10
        (x,y) = app.playerPos
        canvas.create_oval(x-r, y-r, x+r, y+r,
                            fill = "red", outline = "")

    def drawCubes(app, canvas): #draw them in the right order
        color = rgbString(app.bgColor)
        for i in range(len(app.cubes)-1, -1, -1):
            app.cubes[i].draw(app.grid, canvas, color)
    
    def drawPolys(app, canvas): #draw them in the right order
        for i in range(len(app.polys)-1, -1, -1):
            app.polys[i].draw(app.grid, canvas)

    def drawScore(app, canvas):
        margin = 20
        t = f"{app.totalScore}"
        textSize = int(app.width/30)
        f = f"Montserrat {textSize} bold"
        canvas.create_text(margin, margin, text=t, font=f, anchor="nw",fill="white")

    def drawBackground(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill=rgbString(app.bgColor))
    
    def backgroundTick(app):
        ratio = .93
        if app.bgColor == (0,0,0):
            return
        (r,g,b) = app.bgColor
        if r+g+b > 0:
            r,g,b = int(r*ratio),int(g*ratio),int(b*ratio)
        app.bgColor = (r,g,b)
        
    def endSong(app):
        #reset songover screen
        app.app.scoreData = (app.totalScore,app.totalCubes,app.goodSlices,
                            app.badSlices)
        print(app.app.scoreData)
        app.app.songOverMode = SongOver()
        app.app.setActiveMode(app.app.songOverMode)

    def camTick(app):
        output = app.cam.getCoords(app.camThreshold, app.debugMode)
        if(output != None):
            (xScale, yScale) = output
            x = app.width*(1-xScale) #camera's flipped
            y = app.height*yScale
            #add point to blade
            app.blade.insertPoint((x,y))

    def keyPressed(app, event):
        app.bgColor = (100,100,100)

    def closeApp(app):
        print("GAME SHUTDOWN")
        app.running = False

#Learned from:
#cs.cmu.edu/~112/notes/notes-animations-part3.html
class SplashScreen(Mode):
    def appStarted(mode):
        mode.titleText = mode.loadImage("images/titleText.png")
        mode.playButton = mode.loadImage("images/playButton.png")
        mode.playButtonHighlighted = mode.scaleImage(mode.playButton,1.02)
        mode.buttonHighlighted = False
        mode.buttonPos = (mode.width/2, mode.height*.7)

        mode.fading = False
        mode.fadeImg = Image.new('RGB', (mode.width, mode.height), color = 'black')
        mode.fadeIndex = 0

    def redrawAll(mode, canvas):
        cx, cy = mode.width/2,mode.height/2
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        
        canvas.create_image(cx, mode.height*.4, 
                            image=ImageTk.PhotoImage(mode.titleText))
        if mode.buttonHighlighted:
            img = mode.playButtonHighlighted
        else:
            img = mode.playButton
        canvas.create_image(mode.buttonPos, 
                            image=ImageTk.PhotoImage(img))
        
        if mode.fading:
            canvas.create_image(0,0,image=ImageTk.PhotoImage(mode.fadeImgs[mode.fadeIndex]),
                                anchor="nw")

    def fadeOut(mode):
        #load faded images
        mode.fadeImgs = []
        mode.fadeFrames = 10
        for i in range(mode.fadeFrames):
            newIm = mode.fadeImg.copy()
            newIm.putalpha(int((i+1)*255/(mode.fadeFrames)))
            mode.fadeImgs.append(newIm)
        mode.fadeConstant = 0
        mode.fading = True

    def timerFired(mode):
        mode.timerDelay = 1
        if mode.fading and mode.fadeIndex < mode.fadeFrames:
            mode.fadeIndex += 1
            if mode.fadeIndex == mode.fadeFrames:
                mode.app.setActiveMode(mode.app.gameMode)
    '''
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)
    '''
    def mousePressed(mode, event):
        if mode.buttonHighlighted:
            mode.fadeOut()

    def mouseMoved(mode, event):
        if mode.fading:
            return
        width, height = mode.playButton.size
        x,y = mode.buttonPos
        x0, y0 = x-width/2, y-height/2
        x1, y1 = x+width/2, y+height/2
        try:
            if event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1:
                mode.buttonHighlighted = True
            else:
                mode.buttonHighlighted = False
        except:
            pass

#CALL RESET METHOD IN SONGOVER INSTEAD OF REINITALIZING IT
class SongOver(Mode):
    def appStarted(mode):
        #shut down the game
        mode.buttonHighlighted = False
        (mode.score, mode.cubes, mode.good, mode.bad) = mode.app.scoreData
        mode.restartButton = mode.loadImage("images/restartButton.png")
        mode.restartButtonHighlighted = mode.scaleImage(mode.restartButton,1.02)
        mode.buttonPos = (mode.width/2, mode.height*.75)
        mode.app.gameMode.closeApp()
        
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        try:
            mode.drawScoreScreen(canvas)
            if mode.buttonHighlighted:
                img = mode.restartButtonHighlighted
            else:
                img = mode.restartButton
            canvas.create_image(mode.buttonPos, 
                                image=ImageTk.PhotoImage(img))
        except:pass

    def drawScoreScreen(mode, canvas):
        titleFont = "Teko 48 bold"
        songFont = "Teko 36 bold"
        artistFont = "Teko 22 bold"
        t='LEVEL FINISHED'
        canvas.create_text(mode.width/2, mode.height*.3, text=t, 
                            font=titleFont,fill="white")
        t=mode.app.songTitle.upper()
        canvas.create_text(mode.width/2, mode.height*.4, text=t, 
                            font=songFont,fill="white")
        t=mode.app.artist.upper()
        canvas.create_text(mode.width/2, mode.height*.45, text=t, 
                            font=artistFont,fill="gray")
        
        labelF =  "Teko 22 bold"
        c = "gray"
        t="CUBES SLICED"
        canvas.create_text(mode.width*.25, mode.height*.55, text=t,font=labelF,fill=c)
        t="SCORE"
        canvas.create_text(mode.width/2, mode.height*.55, text=t,font=labelF,fill=c)
        t="GOOD CUTS"
        canvas.create_text(mode.width*.75, mode.height*.55, text=t,font=labelF,fill=c)

        numberF1 = "Teko 52 bold"
        numberF2 = "Teko 36 bold"
        c = "white"
        t = f"{mode.good+mode.bad}/{mode.cubes}"
        canvas.create_text(mode.width*.25, mode.height*.56, text=t,font=numberF2,fill=c,anchor="n")
        t = str(mode.score)
        canvas.create_text(mode.width*.5, mode.height*.55, text=t,font=numberF1,fill=c,anchor="n")
        t = f"{mode.good}/{mode.good+mode.bad}"
        canvas.create_text(mode.width*.75, mode.height*.56, text=t,font=numberF2,fill=c,anchor="n")

    def keyPressed(mode, event):
        try:
            mode.app.gameMode = Game()
            mode.app.setActiveMode(mode.app.gameMode)
        except: pass
    
    def mousePressed(mode, event):
        try:
            if mode.buttonHighlighted:
                mode.app.gameMode = Game()
                mode.app.setActiveMode(mode.app.gameMode)
        except: pass

    def mouseMoved(mode, event):
        try:
            width, height = mode.restartButton.size
            x,y = mode.buttonPos
            x0, y0 = x-width/2, y-height/2
            x1, y1 = x+width/2, y+height/2
            if event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1:
                mode.buttonHighlighted = True
            else:
                mode.buttonHighlighted = False
        except:
            pass

class Calibration(Mode):
    pass

class ModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreen()
        app.calibrationMode = Calibration()
        app.song = "Radioactive"
        app.gameMode = Game()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 2

    def closeApp(app):
        pass

class camThread(threading.Thread):
    def __init__(self, threadID, name, game):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game = game

    def run(self):
        while self.game.running:#app._running:
            self.game.camTick()
        print("CAMERA THREAD STOPPED")

def almostEquals(a,b):
    epsilon = 10**-5
    if abs(a-b) <= epsilon:
        return True
    return False
#cmu-112-graphics notes
def rgbString(color):
    (r,g,b) = color
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

#cmu 112 notes: string functions
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

ModalApp(width=1200,height=800)
#Game(width=1200,height=800)