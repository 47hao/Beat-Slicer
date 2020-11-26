
from cmu_112_graphics import *
import slice3d
import grid3d
import random
import convexHull

class Poly3d(object):
    def __init__(self, pos, vel, points):
        self.pos = pos
        self.vel = vel
        self.points = points
        self.faces = self.getFaces()

        self.drawPoints = False
    
    #dictionary of faces
    def getFaces(self):
        return convexHull.getHull(self.points)

    def getPoints(self):
        return self.points
    
    def move(self):
        (x,y,z) = self.pos
        (dx,dy,dz) = self.vel
        self.pos = (x+dx,y+dy,z+dz)
    
    def draw(self, grid, canvas):
        if self.drawPoints:
            r = 5
            color = rgbString(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            globPoints = grid3d.localToGlobal(self.pos, self.points)
            for p in globPoints:
                (x,y) = grid.to2d(p)
                canvas.create_oval(x-r,y-r,x+r,y+r,fill=color)
        
        f,o,w = "", "black", 1 #for wireframe
        c = self.pos
        for face in self.faces:
            facePoints = [self.points[i] for i in face]
            globPoints = grid3d.localToGlobal(c,facePoints)
            #if wireframe or face in self.visibleFaces:
                #localToGlobal these
            converted = []
            for p in globPoints:
                converted.append(grid.to2d(p))
            canvas.create_polygon(converted,fill=f,outline=o, width = w)

#Course Notes 15-112
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'