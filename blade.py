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
            canvas.create_line(x0,y0,x1,y1, width=8, fill="white")

class Spark(object):
    critPoint = 8
    lifeSpan = 12

    def __init__(self, pos, vel):
        (x,y),(dx,dy) = pos,vel
        self.pos1 = (x+dx,y+dy)
        self.pos2 = pos
        self.vel = vel
        self.time = 0
        self.dead = False

    def tick(self):
        if self.time > Spark.lifeSpan:
            self.dead = True
        elif self.time > Spark.critPoint:
            (x,y) = self.pos1
            self.pos1 = (x+dx/4,y+dy/4) #1 goes out 12 total
            (x,y) = self.pos2
            self.pos2 = (x+dx*2,y+dy*2) #2 goes out 8
            #decreasing in size
        else:
            (x,y) = self.pos1
            self.pos1 = (x+dx,y+dy) #1 goes out 8
            (x,y) = self.pos2
            self.pos2 = (x+dx/2,y+dy/2) #2 goes out 4
            #increasing in size
        self.time += 1

    def draw(self, canvas):
        canvas.create_line(self.pos1, self.pos2,width=4,fill="white")

    @staticmethod
    def makeSparks(pos):
        (x,y) = pos
        return Spark(pos,(0,1)) 

def dist(x0,y0,x1,y1):
    dx = (x0-x1)**2
    dy = (y0-y1)**2
    return (dx+dy)**0.5