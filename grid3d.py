
from cmu_112_graphics import *
import cube

class Grid3d(App):
    
    def appStarted(app):
        app.focalLength = 400#min(app.width,app.height)*0.95
        #400 #camera shenanigans

        
        app.timerDelay = 1
        app.ticks = 0
        
        app.cellSize = (app.height*0.8)/3
        app.cubeSize = app.cellSize
        app.rows = 3
        app.cols = 3
        app.deps = 5
        
        app.cubes = []
        #app.makeTestCubes()
    
    def makeTestCubes(app):
        app.cubes += [cube.Cube(60,60,500,50)]
        app.cubes += [cube.Cube(-60,60,500,50)]
        app.cubes += [cube.Cube(60,-60,500,50)]
        app.cubes += [cube.Cube(-60,-60,500,50)]

    def timerFired(app):
        app.ticks += 1
        if(app.ticks*app.timerDelay%100 == 0):
            for i in [-1, 1]:
                for j in [-1, 1]:
                    app.cubes += [cube.Cube(60*i,60*j,2000,60)]

        app.moveCubes()

    def moveCubes(app):
        for cube in app.cubes:
            cube.move(0,0,-8*app.timerDelay)
        app.cleanCubes()
    
    def cleanCubes(app):
        for i in range(len(app.cubes)):
            cube = app.cubes[i]
            if cube.z < -1*app.focalLength-cube.sideLength:
                app.cubes.pop(i)
                print(len(app.cubes))
            else: #frontmost cubes are lowest indices 
                return
                
    def redrawAll(app, canvas):
        #app.drawBackground(canvas)
        #app.drawGrid(canvas)
        app.drawCubes(canvas)
    
    def drawBackground(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")

    def drawCubes(app, canvas): #draw them in the right order
        for i in range(len(app.cubes)-1, -1, -1):
            app.cubes[i].draw(app, canvas, False)

    def drawGrid(app, canvas):
        cx, cy = app.width/2, app.height/2
        for d in range(app.deps):
            #setup scales and cell sizes
            scaleFront = app.perspectiveFactor**(d*app.cellSize)
            scaleBack = app.perspectiveFactor**((d+1)*app.cellSize)
            cellSize = app.cellSize * scaleFront
            cellSizeBack = app.cellSize * scaleBack
            #top left x, y, for front and back
            tx, ty = cx-(app.cols/2)*cellSize, cy-(app.rows/2)*cellSize
            tx2, ty2 = cx-(app.cols/2)*cellSizeBack, cy-(app.rows/2)*cellSizeBack
            for r in range(app.rows):
                for c in range(app.cols):
                    #front square   
                    xf0, yf0 = tx+c*cellSize, ty+r*cellSize
                    xf1, yf1 = xf0+cellSize, yf0+cellSize
                    canvas.create_rectangle(xf0, yf0, xf1, yf1)
                    xb0, yb0 = tx2+c*cellSizeBack, ty2+r*cellSizeBack
                    xb1, yb1 = xb0+cellSizeBack, yb0+cellSizeBack
                    canvas.create_rectangle(xb0, yb0, xb1, yb1)
                    #lists of points for sides drawing
                    pf = [(xf0, yf0),(xf1, yf0),(xf1,yf1),(xf0,yf1)] #clockwise front coords
                    pb = [(xb0, yb0),(xb1, yb0),(xb1,yb1),(xb0,yb1)] #clockwise back coords
                    for i in range(4):
                        pass
                        canvas.create_polygon(pf[i-1],pf[i],pb[i],pb[i-1],
                                            fill="",outline="black")
                    #draw trapezoids
    
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