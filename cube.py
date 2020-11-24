
from cmu_112_graphics import *

class Cube(object):
    #front, top, left, right, bottom, back
    FACES = {"back":(5,4,6,7),"top":(4,5,1,0),
            "left":(4,0,2,6),"right":(1,5,7,3),
            "bottom":(2,3,7,6),"front":(0,1,3,2)}

    def __init__(self,x,y,z,sideLength):
        self.x = x
        self.y = y
        self.z = z
        self.sideLength = sideLength
        self.outlineWidth = 2

        self.vertices = [None]*8
        self.computeVertices()
        self.faces = self.getFaces()
        self.visibleFaces = []
        self.setVisibleFaces()
        
        #self.computeVisibleFaces()

    def getVertices(self):
        return self.vertices
    
    #dictionary of faces
    def getFaces(self):
        result = {}
        index = 0
        for key in Cube.FACES:
            (a,b,c,d) = Cube.FACES[key]
            vs = self.vertices
            result[key] = (vs[a],vs[b],vs[c],vs[d])
            index += 1
        return result
    
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

    def move(self,x,y,z):
        self.x += x
        self.y += y
        self.z += z
        self.computeVertices()
    
    def computeVertices(self):
        s = self.sideLength/2
        counter = 0
        for k in [-1,1]:
            for j in [-1, 1]:
                for i in [-1,1]:
                    self.vertices[counter] = (
                        (self.x+i*s,self.y+j*s,self.z+k*s))
                    counter += 1

    def draw(self, grid, canvas, wireframe):
        #print("drawn")

        if(wireframe):
            faceList = self.getFaces()
        else:
            faceList = self.visibleFaces
        faceList = self.getFaces()
        f = ""
        o = "black"
        w = 1
        if(not(wireframe)):
            f = "white"
            o = "black"
            w = roundHalfUp(0.995**self.z*self.outlineWidth)

        for face in faceList:
            if wireframe or face in self.visibleFaces:
                converted = (grid.to2d(faceList[face][0]),grid.to2d(faceList[face][1]),
                            grid.to2d(faceList[face][2]),grid.to2d(faceList[face][3]))

                canvas.create_polygon(converted,fill=f,outline=o, width = w)

def drawRoundedPoly():
    pass

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


