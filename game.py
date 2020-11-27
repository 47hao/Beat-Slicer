
from cmu_112_graphics import *
import grid3d
import slice3d
import poly3d
import cube

class Game(App):
    def appStarted(app):
        app.focalLength = 400
        app.ticks = 0
        app.timerDelay = 4

        app.cubes = []
        app.polys = []
        cubeSpeed = 2 #absolute speed, pixels/ms
        app.cubeVel = cubeSpeed*app.timerDelay

        app.grid = grid3d.Grid3d(app, app.focalLength)

        #app.testPoly()
        app.addCube((100,0,0),(0,0,0))

        app.mouseDown = False
        app.mousePos1 = None
        app.mousePos2 = None
    
    def mousePressed(app, event):
        app.mouseDown = True
        app.mousePos1 = (event.x,event.y)

    def mouseReleased(app, event):
        app.mouseDown = False
        app.mousePos2 = (event.x,event.y)
        #get plane from mouse pos
        (mx0, my0) = app.mousePos1
        (x0, y0) = (mx0-app.width/2,my0-app.height/2)
        (mx1, my1) = app.mousePos2
        (x1, y1) = (mx1-app.width/2,my1-app.height/2)
        
        plane = slice3d.pointsToPlane((x0,y0,0),(x1,y1,0),(x0,y0,100))
        app.sliceAllCubes(plane)

    def keyPressed(app, event):
        app.testSliceCube()

    def testPoly(app):
        testCube = cube.Cube((100,50,-20),(0,0,0),30)
        points = testCube.getPoints()
        points[3] = (0,-40,0)
        poly = poly3d.Poly3d((100,50,-20),(0,0,-2),points)
        app.polys.append(poly)
    '''
    def testSliceCube(app):
        #polys = app.cubes[0].sliceCube((1,2,0.5,270))
        #polys = app.cubes[0].sliceCube((1,-1.1,0.5,0))
        polys = app.cubes[0].sliceCube((1,-1.1,-.5,50))
        #polys = app.cubes[0].sliceCube((0,0,1,-50))
        if polys == None:
            return
        (poly1, poly2) = polys
        app.cubes.pop(0)
        app.polys.extend([poly1,poly2])
    '''
    def sliceAllCubes(app, plane):
        zoneCounter = 0
        i = 0
        while i < len(app.cubes):
            cube = app.cubes[i]
            if cube.inSliceZone():
                success = app.sliceCube(cube, plane)
                if(not(success)):
                    i += 1
                #move on; didn't slice
            else:
                i += 1
        print("====")
        app.cleanCubes()

    def sliceCube(app,cube, plane):
        print("slice called")
        polys = cube.sliceCube(plane)
        if polys == None:
            return False
        (poly1, poly2) = polys
        app.cubes.pop(app.cubes.index(cube))
        app.polys.extend([poly1,poly2])
        return True

    def makeTestCubes(app):
        app.addCube((0,0,-10),(0,0,-1*app.cubeVel))

    def timerFired(app):
        app.ticks += 1
        app.makeSampleCubePattern()
        app.moveCubes()
    
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
            cube.move()
        for poly in app.polys:
            poly.move()

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
        app.drawSlice(canvas)
    
    def drawSlice(app, canvas):
        if app.mousePos1 != None and app.mousePos2 != None:
            canvas.create_line(app.mousePos1,app.mousePos2)

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