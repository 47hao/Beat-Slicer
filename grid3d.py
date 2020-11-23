
from cmu_112_graphics import *
import cube

class Grid3d(App):
    
    def appStarted(app):
        app.perspectiveFactor = 0.9982 #the distance scales. How?

        
        app.timerDelay = 2
        
        app.cellSize = (app.height*0.8)/3
        app.cubeSize = app.cellSize
        app.rows = 3
        app.cols = 3
        app.deps = 5
        app.makeTestCubes()
    
    def makeTestCubes(app):
        app.cubes = []
        app.cubes += [cube.Cube(60,60,500,60)]
        app.cubes += [cube.Cube(-60,60,500,60)]
        app.cubes += [cube.Cube(60,-60,500,60)]
        app.cubes += [cube.Cube(-60,-60,500,60)]

    def timerFired(app):
        app.moveCubes()

    def moveCubes(app):
        for cube in app.cubes:
            cube.move(0,0,-2*app.timerDelay)
    
    def redrawAll(app, canvas):
        #app.drawGrid(canvas)
        app.drawCubes(canvas)

    def drawCubes(app, canvas):
        for cube in app.cubes:
            cube.draw(app, canvas)

    def drawGrid(app, canvas):
        cx, cy = app.width/2, app.height/2
        for d in range(app.deps):
            #setup scales and cell sizes
            scaleFront = app.perspectiveFactor**(d*app.cellSize)
            scaleBack = app.perspectiveFactor**((d+1)*app.cellSize)
            cellSize = app.cellSize * scaleFront#*app.cellSize
            cellSizeBack = app.cellSize * scaleBack#*app.cellSize
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

    def to2d(app, x,y,z):
        return (app.width/2+x*app.perspectiveFactor**z,
                app.height/2+y*app.perspectiveFactor**z)

    def to2d(app, coords):
        (x,y,z) = coords
        return (app.width/2+x*app.perspectiveFactor**z,
                app.height/2+y*app.perspectiveFactor**z)

    def closeApp(app):
        pass

Grid3d(width=800, height=600)