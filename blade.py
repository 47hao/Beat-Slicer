import time
from cmu_112_graphics import *
#similar to my own code in Fruit Ninja Hack112; rewritten by me, with OOP
#FN Hack112 code overhauled from Ricky Huang's prototype
class Blade(object):
    def __init__(self, game):
        self.points = []
        self.game = game
        self.maxLength = 300
        self.bladeTicks = 0
        self.removeDelay = 2
        self.minPoints = 4
        self.maxPoints = 10
        self.pointTime = 100 #milliseconds

    def bladeStep(self):
        self.bladeTicks += 1
        lengthUsed = 0
        i = 0
        while i < len(self.points):
            startTime = self.points[i][1]
            if (time.time() - startTime)*1000 > self.pointTime:
                self.points.pop(i)
            else:
                i += 1

    def insertPoint(self,p):
        self.points.insert(0,(p,time.time()))
    
    def draw(self, canvas):
        for i in range(len(self.points)-1):
            (x0,y0),(x1,y1) = self.points[i][0], self.points[i+1][0]
            canvas.create_line(x0,y0,x1,y1, width=4, fill="white")
            

def dist(x0,y0,x1,y1):
    dx = (x0-x1)**2
    dy = (y0-y1)**2
    return (dx+dy)**0.5