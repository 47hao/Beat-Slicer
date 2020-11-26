
from cmu_112_graphics import *
import slice3d
import random

class Poly3d(object):
    def __init__(self, pos, vel, points):
        self.pos = pos
        self.vel = vel
        self.points = points
    
    #dictionary of faces
    
    def getPoints(self):
        return self.points
    
    def move(self):
        (x,y,z) = self.pos
        (dx,dy,dz) = self.vel
        self.pos = (x+dx,y+dy,z+dz)
    
    def draw(self, grid, canvas):
        r = 5
        c = rgbString(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        globPoints = grid3d.localToGlobal(self.pos, self.points)
        for p in globPoints:
            (x,y) = grid.to2d(p)
            canvas.create_oval(x-r,y-r,x+r,y+r,fill=c)

#Course Notes 15-112
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'