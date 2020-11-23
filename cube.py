
from cmu_112_graphics import *

class Cube(object):
    #front, top, left, right, bottom, back
    FACES = {"front":(0,1,3,2),"top":(4,5,1,0),
            "left":(4,0,2,6),"right":(1,5,7,3),
            "bottom":(2,3,7,6),"back":(5,4,6,7)}
    def __init__(self,x,y,z,sideLength):
        self.x = x
        self.y = y
        self.z = z
        self.sideLength = sideLength
        
        self.vertices = [None]*8
        self.computeVertices()
        self.faces = self.getFaces()
        self.visibleFaces = [None]*3
        self.computeVisibleFaces()

    def getVertices(self):
        return self.vertices
    
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
        #self.computeVisibleFaces()
    
    def computeVertices(self):
        s = self.sideLength/2
        counter = 0
        for k in [-1,1]:
            for j in [-1, 1]:
                for i in [-1,1]:
                    self.vertices[counter] = (
                        (self.x+i*s,self.y+j*s,self.z+k*s))
                    counter += 1
    
    def computeVisibleFaces(self):
        faces = self.getFaces()
        self.visibleFaces[0] = faces["front"]
        if(self.y >= 0):
            self.visibleFaces[1] = faces["top"]
        else:
            self.visibleFaces[1] = faces["bottom"]
        if(self.x >= 0):
            self.visibleFaces[2] = faces["left"]
        else:
            self.visibleFaces[2] = faces["right"]
        print(self.visibleFaces)
    
    def draw(self, grid, canvas):
        faces = self.getFaces()
        for face in faces:
            converted = (grid.to2d(faces[face][0]),grid.to2d(faces[face][1]),
                        grid.to2d(faces[face][2]),grid.to2d(faces[face][3]))
            canvas.create_polygon(converted,fill="",outline="black")
    
    def drawVisible(self, grid, canvas):
        for face in self.visibleFaces:
            converted = (grid.to2d(face[0]),grid.to2d(face[1]),
                        grid.to2d(face[2]),grid.to2d(face[3]))
            canvas.create_polygon(converted,fill="",outline="black")
    
#cube = Cube(0,0,0,20)
#print(cube.getFaces())


