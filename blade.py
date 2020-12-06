import time
from cmu_112_graphics import *
import random
import math
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
    critPoint = 3
    lifeSpan = 6

    def __init__(self, pos, vel):
        (x,y),(dx,dy) = pos,vel
        self.pos1 = (x+dx,y+dy)
        self.pos2 = pos
        self.vel = vel
        self.time = 0
        self.dead = False
        self.maxWidth = 8
        self.stroke = 1

    def tick(self):
        self.time += 1
        if self.time > Spark.lifeSpan:
            self.dead = True
            return
        self.stroke = int(max(((self.lifeSpan-self.time)/self.lifeSpan),0)*self.maxWidth)
        if self.time > Spark.critPoint:
            (dx,dy) = self.vel
            (x,y) = self.pos1
            self.pos1 = (x+dx/2,y+dy/2) #1 goes out 5 total
            (x,y) = self.pos2
            self.pos2 = (x+dx,y+dy) #2 goes out 4
            #decreasing in size
        else:
            (dx,dy) = self.vel
            (x,y) = self.pos1
            self.pos1 = (x+dx,y+dy) #1 goes out 3
            (x,y) = self.pos2
            self.pos2 = (x+dx/2,y+dy/2) #2 goes out 2
            #increasing in size
        

    def draw(self, canvas):
        canvas.create_line(self.pos1, self.pos2,width=self.stroke,fill="white")

    @staticmethod
    def makeSparks(pos):
        sparkMagnitude = 50
        (x,y) = pos
        sparks = []
        for i in range(12):
            m = random.randint(sparkMagnitude//2, sparkMagnitude)
            angle = random.random()*2*math.pi
            dx,dy = math.cos(angle)*m,math.sin(angle)*m
            sparks.append(Spark(pos,(dx,dy)))
        return sparks

def dist(x0,y0,x1,y1):
    dx = (x0-x1)**2
    dy = (y0-y1)**2
    return (dx+dy)**0.5