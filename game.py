
from cmu_112_graphics import *
import grid3d
import poly3d
import cube

class Game(App):
    def appStarted(app):
        app.focalLength = 400
        app.ticks = 0
        app.timerDelay = 2

        app.cubes = []
        app.polys = []
        cubeSpeed = 6 #absolute speed, pixels/ms
        app.cubeVel = cubeSpeed*app.timerDelay

        app.grid = grid3d.Grid3d(app, app.focalLength)

        #app.testPoly()
        app.testSliceCube()
    
    def testPoly(app):
        testCube = cube.Cube((100,50,-20),(0,0,0),30)
        points = testCube.getPoints()
        points[3] = (0,-40,0)
        poly = poly3d.Poly3d((100,50,-20),(0,0,-2),points)
        app.polys.append(poly)

    def testSliceCube(app):
        app.addCube((100,100,-50),(0,0,0))
        (poly1, poly2) = app.cubes[0].sliceCube((1,2,0,300))
        #app.cubes.pop(0)
        app.polys.extend([poly1,poly2])

    def makeTestCubes(app):
        app.addCube((0,0,-10),(0,0,-1*app.cubeVel))

    def timerFired(app):
        app.ticks += 1
        #app.makeSampleCubePattern()
        app.moveCubes()
    
    def makeSampleCubePattern(app):
        if(app.ticks*app.timerDelay%300 == 0):
            for row in [-1,0,1]:
                for col in [-1,1]:
                    (x,y) = app.grid.getLaneCoords(row, col)
                    app.addCube((x,y,app.grid.startZ),
                                (0,0,-1*app.cubeVel))
        if(app.ticks*app.timerDelay%300 == 150):
            for row in [-1, 1]:
                for col in [-1, 0, 1]:
                    (x,y) = app.grid.getLaneCoords(row, col)
                    app.addCube((x,y,app.grid.startZ),
                                (0,0,-1*app.cubeVel))
    
    def addCube(app, pos, vel):
        app.cubes.append(cube.Cube(pos, vel, app.grid.cubeSize))

    def moveCubes(app):
        for cube in app.cubes:
            cube.move()
        app.cleanCubes()
    
    def cleanCubes(app):
        i = 0
        while i < len(app.cubes):
            cube = app.cubes[i]
            if cube.pos[2] < -1*app.focalLength-cube.sideLength:
                app.cubes.pop(i)
                #print(len(app.cubes))
            else: #frontmost cubes are lowest indices 
                return

    def redrawAll(app, canvas):
        #app.drawBackground(canvas)
        #app.drawGrid(canvas)
        #canvas.create_rectangle(10,10,10+app.cubeSize,10+app.cubeSize)
        app.drawCubes(canvas)
        app.drawPolys(canvas)
    
    def drawCubes(app, canvas): #draw them in the right order
        for i in range(len(app.cubes)-1, -1, -1):
            app.cubes[i].draw(app.grid, canvas, True)
    
    def drawPolys(app, canvas): #draw them in the right order
        for i in range(len(app.polys)-1, -1, -1):
            app.polys[i].draw(app.grid, canvas)

    def drawBackground(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    
    def closeApp(app):
        pass



Game(width=800,height=600)