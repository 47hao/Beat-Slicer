
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
        
        self.vertices = [None]*8
        self.computeVertices()
        self.faces = self.getFaces()
        self.visibleFaces = {}
        
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
    '''
    #destructive
    def computeVisibleFaces(self):
        vFaces = {}#self.visibleFaces
        vFaces["front"] = self.faces["front"]
        if(self.y >= 0):
            vFaces["top"] = self.faces["top"]
            vFaces["bottom"] = None
        else:
            vFaces["bottom"] = self.faces["bottom"]
            vFaces["top"] = None
        if(self.x >= 0):
            vFaces["left"] = self.faces["left"]
            vFaces["right"] = None
        else:
            vFaces["right"] = self.faces["right"]
            vFaces["left"] = None
        self.visibleFaces = vFaces
        #print(self.visibleFaces)
    '''
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

        if(not(wireframe)): #eliminate unseen faces
            f = "white"
            o = "black"
            w = roundHalfUp(0.995**self.z*2)
            #eliminate 
            if(self.y >= 0):
                faceList["bottom"] = None
            else:
                faceList["top"] = None
            if(self.x >= 0):
                faceList["right"] = None
            else:
                faceList["left"] = None
            faceList["back"] = None

        #KEY PROBLEM: FACE DRAWING BADLY
        #sometimes only 2 faces are visible...
        #compare if x>y, then set a face order somehow???

        #now draw all faces
        #MUST DRAW FRONT FACE LAST
        for face in faceList:
            if(faceList[face] != None):
                converted = (grid.to2d(faceList[face][0]),grid.to2d(faceList[face][1]),
                            grid.to2d(faceList[face][2]),grid.to2d(faceList[face][3]))
                canvas.create_polygon(converted,fill=f,outline=o, width = w)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#cube = Cube(0,0,0,20)
#print(cube.getFaces())


