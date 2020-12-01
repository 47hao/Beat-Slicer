import cube

class BeatCube(cube.Cube):
    def __init__(self,grid,cubeParams,targetBeat,preBeats):
        (pos,vel,sideLength) = cubeParams
        super().__init__(pos,vel,sideLength)
        self.grid = grid
        self.targetBeat = targetBeat
        self.prespawnBeats = preBeats
    
    def updatePos(self, grid, beat):
        (x,y,z) = self.pos
        z = ((self.targetBeat-beat)/self.prespawnBeats)*self.grid.startZ
        self.pos = (x,y,z)


