
from cmu_112_graphics import *
import cube

class Grid3d(App):
    
    def appStarted(app):
        app.focalLength = 400#min(app.width,app.height)*0.95

        app.timerDelay = 1
        app.ticks = 0

        app.startZ = 3000
        app.gridWidth = min(app.width,app.height)*2/3
        app.gridSize = app.gridWidth/3

        app.cubeSize = app.gridSize*0.7
        app.cubeSpeed = 10
        
        app.cubes = []
        #app.makeTestCubes()
        

    def getLaneCoords(app, row, col):
        return row*app.gridSize, col*app.gridSize

    def makeTestCubes(app):
        app.cubes += [cube.Cube(0,0,-10,app.cubeSize)]
        #app.cubes += [cube.Cube(-60,60,500,60)]
        #app.cubes += [cube.Cube(60,-60,500,30)]
        #app.cubes += [cube.Cube(-60,-60,500,60)]

    def timerFired(app):
        app.ticks += 1
        app.makeSampleCubePattern()
        app.moveCubes()

    def makeSampleCubePattern(app):
        if(app.ticks*app.timerDelay%200 == 0):
            for row in [-1,0,1]:
                for col in [-1,1]:
                    (x,y) = app.getLaneCoords(row, col)
                    app.cubes += [cube.Cube(x,y,app.startZ,app.cubeSize)]
        if(app.ticks*app.timerDelay%200 == 100):
            for row in [-1, 1]:
                for col in [-1, 0, 1]:
                    (x,y) = app.getLaneCoords(row, col)
                    app.cubes += [cube.Cube(x,y,app.startZ,app.cubeSize)]
                    
    def moveCubes(app):
        for cube in app.cubes:
            cube.move(0,0,-1*app.cubeSpeed*app.timerDelay)
        app.cleanCubes()
    
    def cleanCubes(app):
        i = 0
        while i < len(app.cubes):
            cube = app.cubes[i]
            if cube.z < -1*app.focalLength-cube.sideLength:
                app.cubes.pop(i)
                #print(len(app.cubes))
            else: #frontmost cubes are lowest indices 
                return
                
    def redrawAll(app, canvas):
        #app.drawBackground(canvas)
        #app.drawGrid(canvas)
        #canvas.create_rectangle(10,10,10+app.cubeSize,10+app.cubeSize)
        app.drawCubes(canvas)

    def drawBackground(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")

    def drawCubes(app, canvas): #draw them in the right order
        for i in range(len(app.cubes)-1, -1, -1):
            app.cubes[i].draw(app, canvas, True)

    def keyPressed(app, event):
        mvtSpeed = 5
        if event.key == "Up":
            app.cube.move(0,-1*mvtSpeed,0)
        elif event.key == "Down":
            app.cube.move(0,1*mvtSpeed,0)
        elif event.key == "Left":
            app.cube.move(-1*mvtSpeed,0,0)
        elif event.key == "Right":
            app.cube.move(1*mvtSpeed,0,0)
        elif event.key == "w":
            app.cube.move(0,0,1*mvtSpeed)
        elif event.key == "s":
            app.cube.move(0,0,-1*mvtSpeed)

    #Hand calculated method
    def to2d(app, coords):
        (x,y,z) = coords
        f = app.focalLength
        
        epsilon = 10**-10
        if(z <= -1*app.focalLength):
            z = -1*app.focalLength+epsilon
        #clips bad z values
        #SIMPLE (and inaccurate) SOLUTION:
        #x1 = app.width/2+f*x/z
        #y1 = app.height/2+f*y/z

        x1 = app.width/2+f*x/(z+f)
        y1 = app.height/2+f*y/(z+f)
        return (x1,y1)
    
    def closeApp(app):
        pass



Grid3d(width=800, height=600)