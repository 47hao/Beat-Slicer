
from cmu_112_graphics import *
import slice3d
import grid3d
import poly3d

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
        self.outlineWidth = 2

        self.faces = dict()
        self.setFaces()
        self.faceOrder = []
        self.orderFaces()

        self.sliceVel = 0.3

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
        #
        result.append("front")
        self.faceOrder = result

    def draw(self, grid, canvas, wireframe):
        (x,y,z) = self.pos
        #fill, outline, width
        f,o,w = "", "black", 1 #for wireframe
        if(not(wireframe)):
            f,o = "white", "black"
            w = roundHalfUp(0.995**z*self.outlineWidth)

        if(abs(z) < self.sideLength): #indicate cube is in slice zone
            f = "green"

        #reassemble/reorder faceList?
        c = self.pos #centroid
        for faceName in self.faceOrder:
            globPoints = grid3d.localToGlobal(c,self.faces[faceName])
            #if wireframe or face in self.visibleFaces:
                #localToGlobal these
            converted = []
            for p in globPoints:
                converted.append(grid.to2d(p))
            canvas.create_polygon(converted,fill=f,outline=o, width = w)
    
    def sliceCube(self, plane):
        glob = grid3d.localToGlobal(self.pos, self.points)
        #print("global points:",glob)
        sliced = slice3d.slicePoly(glob,self.EDGES,plane)
        if sliced == None:
            return None
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
