
from cmu_112_graphics import *
import grid3d
import slice3d
import poly3d
import cube
import blade

import camTracker
import threading

class Game(App):
    def appStarted(app):
        app.debugMode = True
        app.maxThreads = 4
        app.runThreads = True

        app.focalLength = 400
        app.ticks = 0
        app.timerDelay = 1

        app.cubes = []
        app.polys = []
        cubeSpeed = 8 #pixels/ms, inaccurate due to timer
        app.cubeVel = cubeSpeed*app.timerDelay

        app.grid = grid3d.Grid3d(app, app.focalLength)

        #app.testPoly()
        app.addCube((100,0,0),(0,0,0))

        app.blade = blade.Blade(app)

        app.camThreshold = .9
        app.cam = camTracker.camTracker()
        app.playerPos = (0,0)

        cThread = camThread(1, "camThread", app)
        cThread.start()
        #mThread = moveThread(1, "moveThread", app)
        #mThread.start()
    
    def timerFired(app):
        app.ticks += 1
        app.blade.bladeStep()
        app.makeSampleCubePattern()
        app.moveCubes()
        app.bladeSlice()
        if(app.debugMode):
            app.cam.showFrame()

    def camTick(app):
        output = app.cam.getCoords(app.camThreshold, app.debugMode)
        if(output != None):
            (xScale, yScale) = output
            x = app.width*(1-xScale) #camera's flipped
            y = app.height*yScale
            #add point to blade
            app.blade.points.insert(0,(x,y))
    
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
            (x0,y0), (x1,y1) = app.blade.points[i], app.blade.points[i+1]
            #convert coords to 3-space and not screen space
            app.sliceAllCubes((x0-app.width/2,y0-app.height/2),
                                (x1-app.width/2,y1-app.height/2))

    def sliceAllCubes(app, p0, p1):
        (x0,y0),(x1,y1) = p0, p1
        plane = slice3d.pointsToPlane((x0,y0,0),(x1,y1,0),(0,0,-1000))
        i = 0
        while i < len(app.cubes):
            cube = app.cubes[i]
            if cube.inSliceZone() and cube.lineInCube(p0, p1):
                #should always work
                success = app.sliceCube(cube, plane)
                #success = 
                if(not(success)):
                    i += 1
                #move on; didn't slice
            else:
                i += 1
        app.cleanCubes()

    def sliceCube(app,cube, plane):
        polys = cube.sliceCube(plane)
        if polys == None:
            return False
        (poly1, poly2) = polys
        app.cubes.pop(app.cubes.index(cube))
        app.polys.extend([poly1,poly2])
        return True

    def makeTestCubes(app):
        app.addCube((0,0,-10),(0,0,-1*app.cubeVel))

    
    def makeSampleCubePattern(app):
        if(app.ticks*app.timerDelay%600 == 0):
            for row in [-1,0,1]:
                for col in [-1,1]:
                    (x,y) = app.grid.getLaneCoords(row, col)
                    app.addCube((x,y,app.grid.startZ),
                                (0,0,-1*app.cubeVel))
        if(app.ticks*app.timerDelay%600 == 300):
            for row in [-1, 1]:
                for col in [-1, 0, 1]:
                    (x,y) = app.grid.getLaneCoords(row, col)
                    app.addCube((x,y,app.grid.startZ),
                                (0,0,-1*app.cubeVel))
    
    def makeSampleCubePattern2(app):
        if(app.ticks*app.timerDelay%600 == 0):
            for col in [-1,1]:
                (x,y) = app.grid.getLaneCoords(0, col)
                app.addCube((x,y,app.grid.startZ),
                                (0,0,-1*app.cubeVel))
        if(app.ticks*app.timerDelay%600 == 300):
            for row in [-1, 1]:
                (x,y) = app.grid.getLaneCoords(row, 0)
                app.addCube((x,y,app.grid.startZ),
                            (0,0,-1*app.cubeVel))

    def addCube(app, pos, vel):
        app.cubes.append(cube.Cube(pos, vel, app.grid.cubeSize))

    def moveCubes(app):
        for cube in app.cubes:
            cube.move(app.timerDelay)
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

    def redrawAll(app, canvas):
        #app.drawBackground(canvas)
        #app.drawGrid(canvas)
        #canvas.create_rectangle(10,10,10+app.grid.cubeSize,10+app.grid.cubeSize)
        app.drawCubes(canvas)
        app.drawPolys(canvas)
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
        for i in range(len(app.cubes)-1, -1, -1):
            app.cubes[i].draw(app.grid, canvas, False)
    
    def drawPolys(app, canvas): #draw them in the right order
        for i in range(len(app.polys)-1, -1, -1):
            app.polys[i].draw(app.grid, canvas)

    def drawBackground(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    
    def closeApp(app):
        pass

class camThread(threading.Thread):
    def __init__(self, threadID, name, game):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game = game

    def run(self):
        while self.game._running:
            self.game.camTick()
'''
class moveThread(threading.Thread):
    def __init__(self, threadID, name, game):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game = game

    def run(self):
        while self.game._running:
            self.game.moveCubes()
'''
Game(width=800,height=600)