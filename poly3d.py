
from cmu_112_graphics import *
import slice3d

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