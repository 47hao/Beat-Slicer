
from cmu_112_graphics import *
import slice3d
import grid3d
import poly3d
import convexHull

class Cube(poly3d.Poly3d):
    #front, top, left, right, bottom, back
    FACES = {"back":(5,4,6,7),"top":(4,5,1,0),
            "left":(4,0,2,6),"right":(1,5,7,3),
            "bottom":(2,3,7,6),"front":(0,1,3,2)}
    EDGES = {(0,1),(1,3),(3,2),(2,0),(0,4),(2,6),(1,5),(3,7),
            (4,5),(5,7),(7,6),(6,4)}

    def __init__(self,pos,vel,sideLength):
        self.sideLength = sideLength
        self.points = getCubePoints(sideLength)
        super().__init__(pos, vel, self.points)
        self.outlineWidth = 8

        self.faces = dict()
        self.setFaces()
        self.faceOrder = []
        self.orderFaces()

        self.sliceVel = 8

    #if z is sliceable
    def inSliceZone(self):
        return abs(self.pos[2]) <= self.sideLength*2

    def move(self, timerDelay): #no gravity
        (x,y,z) = self.pos
        (dx,dy,dz) = self.vel
        self.pos = (x+dx,y+dy,z+dz)

    #dictionary of faces
    def setFaces(self):
        #destructive
        for key in Cube.FACES:
            (a,b,c,d) = Cube.FACES[key]
            self.faces[key] = (self.points[a],self.points[b],
                                self.points[c],self.points[d])
                                
    #faces cannot be ordered purely on position
    def orderFaces(self):
        result = []
        result.append("back")
        #first add the rear face
        (x,y,z) = self.pos
        if abs(x) < self.sideLength/2:
            result.append("right")
            result.append("left")
            nextSideFace = None
        elif x > 0:
            result.append("right")
            nextSideFace = "left"
        else:
            result.append("left")
            nextSideFace = "right"

        if abs(y) < self.sideLength/2:
            result.append("top")
            result.append("bottom")
            nextTopFace = None
        elif y > 0:
            result.append("bottom")
            nextTopFace = "top"
        else:
            result.append("top")
            nextTopFace = "bottom"
        if(nextTopFace != None):
            result.append(nextTopFace)
        if(nextSideFace != None):
            result.append(nextSideFace)
        result.append("front")
        self.faceOrder = result
        
    def draw(self, grid, canvas, color):
        (x,y,z) = self.pos
        #fill, outline, width
        w = roundHalfUp(abs((grid.startZ-z)/grid.startZ)*self.outlineWidth)
        #get 2D points from 3D
        c = self.pos
        polyPoints = []
        frontPoints = []
        for faceName in self.faceOrder:
            globPoints = grid3d.localToGlobal(c,self.faces[faceName])
            for p in globPoints:
                polyPoints.append(grid.to2d(p))
            if faceName == "front":
                for p in globPoints:
                    frontPoints.append(grid.to2d(p))
        #get polygon from 2D shapes
        pointIndices = convexHull.get2dHull(polyPoints)
        drawPoly = []
        for i in pointIndices:
            drawPoly.append(polyPoints[i])
        #get front face points
        ((x0,y0),(x1,y1),(x2,y2),(x3,y3)) = frontPoints
        frontPoints = ((x0+w,y0+w),(x1-w,y1+w),(x2-w,y2-w),(x3+w,y3-w))
        #draw polygon
        canvas.create_polygon(drawPoly,fill="white",outline=color, width = w)
        canvas.create_polygon(frontPoints,fill=color,outline="")

    def sliceCube(self, plane):
        glob = grid3d.localToGlobal(self.pos, self.points)
        #print("global points:",glob)
        sliced = slice3d.slicePoly(glob,self.EDGES,plane)
        
        if sliced == None:
            return None
        #print("i am sliced")
        (points1, points2) = sliced
        loc1 = grid3d.globalToLocal(self.pos, points1)
        loc2 = grid3d.globalToLocal(self.pos, points2)
        #get velocity
        (dx, dy, dz) = self.vel
        (i0,j0,k0,d) = plane
        (i1,j1,k1) = getUnitVector(i0,j0,k0)
        v = self.sliceVel
        vel1 = (dx+i1*v, dy+j1*v, dz+k1*v)
        vel2 = (dx-i1*v, dy-j1*v, dz-k1*v)
        poly1 = poly3d.Poly3d(self.pos, vel1, loc1)
        poly2 = poly3d.Poly3d(self.pos, vel2, loc2)
        return poly1, poly2

    def lineInCube(self, p0, p1):
        (x,y,z) = self.pos
        s = self.sideLength/2
        points = [(x-s,y-s),(x+s,y-s),(x+s,y+s),(x-s,y+s)]
        for i in range(4):
            q0, q1 = points[i], points[i-1]
            if checkLineIntersect(q0,q1,p0,p1):
                return True
        return False


#checkIntersect general algorithm based on code by Ansh Riyal
#https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def checkLineIntersect(a0, a1, b0, b1): #lines (a0 -> a1) and (b0 -> b1)
    o1 = orientation(a0, a1, b0)
    o2 = orientation(a0, a1, b1)
    o3 = orientation(b0, b1, a0)
    o4 = orientation(b0, b1, a1)
    if o1 != o2 and o3 != o4:
        return True
    return False

def orientation(a,b,c):
    (x0,y0),(x1,y1),(x2,y2) = a,b,c
    value = ((y1-y0) * (x2-x1) - (x1-x0) * (y2-y1))
    if value > 0:
        return "counterClock"
    elif value < 0:
        return "clock"
    else:
        return "colinear"


def getUnitVector(i,j,k):
    d = (i**2+j**2+k**2)**0.5
    return (i/d, j/d, k/d)

def getCubePoints(sideLen):
    s = sideLen/2
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
    testCube = Cube((0,0,0),(0,0,0),30)
    print(slice3d.slicePoly(testCube.getPoints(),testCube.EDGES,(0,0,1,2)))

#testSlicePoly()
#testFuncs()
