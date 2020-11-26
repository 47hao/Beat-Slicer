import cube

class Grid3d(object):
    
    def __init__(self, game, focal):
        self.focalLength = focal#min(app.width,app.height)*0.95
        self.game = game

        self.startZ = 3000
        self.gridWidth = min(game.width,game.height)*2/3
        self.gridSize = self.gridWidth/3
        self.cubeSize = self.gridSize*0.7
        self.cubes = []
        #app.makeTestCubes()

    def getLaneCoords(self, row, col):
        return row*self.gridSize, col*self.gridSize
                    
    def moveCubes(self):
        for cube in self.cubes:
            cube.move()
        self.cleanCubes()
    
    def cleanCubes(self):
        i = 0
        while i < len(self.cubes):
            cube = self.cubes[i]
            if cube.pos[2] < -1*self.focalLength-cube.sideLength:
                self.cubes.pop(i)
                #print(len(app.cubes))
            else: #frontmost cubes are lowest indices 
                return

    def addCube(self,pos,vel):
        self.cubes.append(cube.Cube(pos, vel, self.cubeSize))

    def drawCubes(self, game, canvas): #draw them in the right order
        for i in range(len(self.cubes)-1, -1, -1):
            self.cubes[i].draw(self, canvas, True)

    #Hand calculated method
    def to2d(self, coords):
        (x,y,z) = coords
        f = self.focalLength
        
        epsilon = 10**-10

        if(z <= -1*self.focalLength):
            z = -1*self.focalLength+epsilon
        #clips bad z values
        #SIMPLE (and inaccurate) SOLUTION:
        #x1 = app.width/2+f*x/z
        #y1 = app.height/2+f*y/z

        x1 = self.game.width/2+f*x/(z+f)
        y1 = self.game.height/2+f*y/(z+f)
        return (x1,y1)
    
