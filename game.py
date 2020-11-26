
from cmu_112_graphics import *
import grid3d
import cube

class Game(App):
    def appStarted(app):
        app.focalLength = 400
        app.ticks = 0
        app.timerDelay = 2

        cubeSpeed = 6 #absolute speed, pixels/ms
        app.cubeVel = cubeSpeed*app.timerDelay

        app.grid = grid3d.Grid3d(app, app.focalLength)

        app.testSliceCube()

    def testSliceCube(app):
        app.grid.addCube((0,0,-10),(0,0,0))
        app.grid.addCube((0,0,-10),(0,0,0))

    def makeTestCubes(app):
        app.grid.addCube((0,0,-10),(0,0,-1*app.cubeVel))

    def timerFired(app):
        app.ticks += 1
        #app.makeSampleCubePattern()
        app.grid.moveCubes()
    
    def makeSampleCubePattern(app):
        if(app.ticks*app.timerDelay%300 == 0):
            for row in [-1,0,1]:
                for col in [-1,1]:
                    (x,y) = app.grid.getLaneCoords(row, col)
                    app.grid.addCube((x,y,app.grid.startZ),
                                    (0,0,-1*app.cubeVel))
        if(app.ticks*app.timerDelay%300 == 150):
            for row in [-1, 1]:
                for col in [-1, 0, 1]:
                    (x,y) = app.grid.getLaneCoords(row, col)
                    app.grid.addCube((x,y,app.grid.startZ),
                                    (0,0,-1*app.cubeVel))
    
    def redrawAll(app, canvas):
        #app.drawBackground(canvas)
        #app.drawGrid(canvas)
        #canvas.create_rectangle(10,10,10+app.cubeSize,10+app.cubeSize)
        app.grid.drawCubes(app,canvas)
    
    def drawBackground(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    
    def closeApp(app):
        pass



Game(width=800,height=600)