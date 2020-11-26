import cube

class Grid3d(object):
    
    def __init__(self, game, focal):
        self.focalLength = focal#min(app.width,app.height)*0.95
        self.game = game

        self.startZ = 3000
        self.gridWidth = min(game.width,game.height)*2/3
        self.gridSize = self.gridWidth/3
        self.cubeSize = self.gridSize*0.7
        #app.makeTestCubes()

    def getLaneCoords(self, row, col):
        return row*self.gridSize, col*self.gridSize

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


#center of mass, use it to find global
def localToGlobal(centroid,points):
    #print(points)
    #print("type:", type(points))
    (x,y,z) = centroid
    result = []
    for (x0,y0,z0) in points:
        result.append((x0+x,y0+y,z0+z))
    return result

#center of mass, shift points to it
def globalToLocal(centroid,points):
    (x,y,z) = centroid
    result = []
    for (x0,y0,z0) in points:
        result.append((x0-x,y0-y,z0-z))
    return result
    
