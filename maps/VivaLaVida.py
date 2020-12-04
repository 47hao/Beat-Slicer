class Beat(object):
    def __init__(self,beat,pos,direc):
        self.beat = beat
        self.pos = pos
        self.direc = direc
    def __repr__(self):
        return f"\n{self.beat},{self.pos},{self.direc}"

def intro(startBeat):
    s = startBeat
    return [Beat(s,(0,1),'l'),
            Beat(s+1,(1,1),'r'),
            Beat(s+2,(0,1),'l'),
            Beat(s+3,(1,1),'r'),
            Beat(s+3.5,(1,0),'u'),
            Beat(s+4.5,(1,0),'d')]

def beatMap():
    beatMap = [] + intro(8)
    return beatMap
