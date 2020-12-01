import cube

class BeatCube(cube.Cube):
    def __init__(self,grid,cubeParams,targetBeat,speed):
        (pos,vel,sideLength) = cubeParams
        super().__init__(pos,vel,sideLength)
        self.grid = grid
        self.targetBeat = targetBeat
        self.prespawnBeats = grid.startZ/speed
    
    def updatePos(self, grid, beat):
        z = ((targetBeat-beat)/self.prespawnBeats)*self.grid.startZ

