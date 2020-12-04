import cube
import grid3d

class BeatCube(cube.Cube):
    def __init__(self,grid,cubeParams,direction,targetBeat,preBeats):
        (pos,vel,sideLength) = cubeParams
        super().__init__(pos,vel,sideLength)
        self.grid = grid
        self.targetBeat = targetBeat
        self.prespawnBeats = preBeats
        self.direction = direction
    
    def updatePos(self, grid, beat):
        (x,y,z) = self.pos
        z = ((self.targetBeat-beat)/self.prespawnBeats)*self.grid.startZ
        self.pos = (x,y,z)
    
    def draw(self, grid, canvas, wireframe):
        super().draw(grid, canvas, wireframe)

        (x,y,z) = self.pos

        c = self.pos #centroid
        globPoints = grid3d.localToGlobal(c,self.faces["front"])
        converted = []
        for p in globPoints:
            converted.append(grid.to2d(p))

        self.drawArrow(converted, canvas)
    
    def checkDir(self, p0, p1):
        (x0, y0),(x1,y1) = p0, p1 
        if x1 == x0:
            denom = 10^-10
        else:
            denom = x1-x0
        slope = (y1-y0)/denom
        if self.direction == "down":
            return abs(slope) > 1 and y1>y0
        elif self.direction == "up":
            return abs(slope) > 1 and y1<y0
        elif self.direction == "left":
            return abs(slope) < 1 and x1>x0
        elif self.direction == "right":
            return abs(slope) < 1 and x1<x0

    def drawArrow(self, points, canvas):
        #print(points)
        (p0, p1, p2, p3) = points
        #p0---p1
        # |   |
        #p3---p2
        #calculate reusable corners
        width = p1[0] - p0[0]
        m = width/8 #margin
        c0, c1 = (p0[0]+m,p0[1]+m),(p1[0]-m,p1[1]+m)
        c2, c3 = (p2[0]-m,p2[1]-m),(p3[0]+m,p3[1]-m)
        b = m/2 #arrow body height
        p = m*2 #arrow tip size
        if self.direction == "down":
            midX = (c0[0]+c1[0])//2
            arrowPoints = [ c0,c1,(c1[0],c1[1]+b),
                (midX, c0[1]+b+p),(c0[0],c0[1]+b)]
        elif self.direction == "up":
            midX = (c0[0]+c1[0])//2
            arrowPoints = [ c3,c2,(c2[0],c2[1]-b),
                (midX, c2[1]-b-p),(c3[0],c3[1]-b)]
        elif self.direction == "left":
            midY = (c1[1]+c2[1])//2
            arrowPoints = [c1,c2,(c2[0]-b,c2[1]),
                (c2[0]-b-p, midY),(c1[0]-b,c1[1])]
        elif self.direction == "right":
            midY = (c1[1]+c2[1])//2
            arrowPoints = [c0,c3,(c3[0]+b,c3[1]),
                (c0[0]+b+p, midY),(c0[0]+b,c0[1])]
        canvas.create_polygon(arrowPoints,fill="black")




