
from cmu_112_graphics import *
import slice3d

class Poly3d(object):
    #front, top, left, right, bottom, back
    FACES = {"back":(5,4,6,7),"top":(4,5,1,0),
            "left":(4,0,2,6),"right":(1,5,7,3),
            "bottom":(2,3,7,6),"front":(0,1,3,2)}
    EDGES = {(0,1),(1,3),(3,2),(2,0),(0,4),(2,6),(1,5),(3,7)}

    def __init__(self,x,y,z,sideLength):
        self.x = x
        self.y = y
        self.z = z
        self.sideLength = sideLength
        self.outlineWidth = 2

        self.points = getCubePoints(sideLength)
        self.faces = dict()
        self.setFaces()
        self.faceOrder = []
        self.orderFaces()
        #self.setVisibleFaces()
        
        #self.computeVisibleFaces()
    
    #dictionary of faces
    def setFaces(self):
        #result = {}
        for key in Cube.FACES:
            (a,b,c,d) = Cube.FACES[key]
            #points = slice3d.localToGlobal((self.x,self.y,self.z),
            #                            self.points) 
            self.faces[key] = (self.points[a],self.points[b],
                                self.points[c],self.points[d])
        #return result
    
    def getPoints(self):
        return self.points
    #faces cannot be ordered purely on position
    def orderFaces(self):
        result = []
        result.append("back")
        #first add the rear face
        if abs(self.x) < self.sideLength/2:
            result.append("right")
            result.append("left")
            nextSideFace = None
        elif self.x > 0:
            result.append("right")
            nextSideFace = "left"
        else:
            result.append("left")
            nextSideFace = "right"

        if abs(self.y) < self.sideLength/2:
            result.append("top")
            result.append("bottom")
            nextTopFace = None
        elif self.y > 0:
            result.append("bottom")
            nextTopFace = "top"
        else:
            result.append("top")
            nextTopFace = "bottom"
        if(nextTopFace != None):
            result.append(nextTopFace)
        if(nextSideFace != None):
            result.append(nextSideFace)
        #
        result.append("front")
        self.faceOrder = result
    '''
    def setVisibleFaces(self):
        if self.x > self.sideLength/2:
            self.visibleFaces.append("left")
        if self.x < -1*self.sideLength/2:
            self.visibleFaces.append("right")
        if self.y > self.sideLength/2:
            self.visibleFaces.append("top")
        if self.y < -1*self.sideLength/2:
            self.visibleFaces.append("bottom")
        self.visibleFaces.append("front")
    '''
    def move(self,x,y,z):
        self.x += x
        self.y += y
        self.z += z
        #self.setFaces()

    def draw(self, grid, canvas, wireframe):
        #print("drawn")
        #faceList = self.faces
        f = ""
        o = "black"
        w = 1
        if(not(wireframe)):
            f = "white"
            o = "black"
            w = roundHalfUp(0.995**self.z*self.outlineWidth)

        if(abs(self.z) < self.sideLength):
            f = "green"

        #reassemble/reorder faceList?
        c = (self.x,self.y,self.z) #centroid
        for faceName in self.faceOrder:
            globPoints = slice3d.localToGlobal(c,self.faces[faceName])
            #if wireframe or face in self.visibleFaces:
                #localToGlobal these
            converted = []
            for p in globPoints:
                converted.append(grid.to2d(p))
            '''
            converted = [grid.to2d(globPoints[0]),
                         grid.to2d(globPoints[1]),
                         grid.to2d(globPoints[2]),
                         grid.to2d(globPoints[3])]
            '''
            canvas.create_polygon(converted,fill=f,outline=o, width = w)
    
def getCubePoints(side):
    s = side/2
    result = []
    for z in [-1]:
        for y in [-1,1]:
            for x in [-1,1]:
                result.append((x*s,y*s,z*s))
    result.append((-1*s,-1*s,1*s))
    result.append((1*s,-1*s,1*s))
    result.append((-1*s,1*s,1*s))
    result.append((1*s,1*s,1*s))
    return result

def drawRoundedPoly():
    pass

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def testFuncs():
    print(getCubePoints(10))
    print(getCubePoints(100))

def testSlicePoly():
    testCube = Cube(0,0,0,30)
    print(slice3d.slicePoly(testCube.getPoints(),testCube.EDGES,(0,0,1,2)))

testSlicePoly()
#testFuncs()
