#Map format inspired by:
#https://bsmg.wiki/mapping/map-format.html
#HELPER FUNCTIONS FOR MAPPING
#===============================================================================
class Beat(object):
    def __init__(self,beat,pos,direc):
        self.beat,self.pos,self.direc = beat,pos,direc
    def __repr__(self):
        return f"\n{self.beat},{self.pos},{self.direc}"

def mirrored(beats):
    result = []
    for beat in beats:
        beat, (x,y), direc = beat.beat, beat.pos, beat.direc
        result.append(Beat(b,(x*-1,y),direc))
    return result

def getData():
    return bpm, offset, beatMap(), fileName, songName, artist, 0
#=============================================================================

bpm = 138
offset = 1.7
fileName = "VivaShort.wav"
songName = "Viva La Vida"
artist = "Coldplay"

def beatLine(startBeat):
    locs = (1,-1)
    dirs = ('r','l')
    return [Beat(startBeat+s*2, ((locs[s%2]-0.5)*2,1), dirs[s%2]) for s in range(0,4)]

def tune(startBeat):
    s = startBeat
    return [Beat(s,(1,1),'r'),
            Beat(s+1,(-1,1),'l'),
            Beat(s+2,(1,1),'r'),
            Beat(s+3,(-1,1),'l'),
            Beat(s+4,(1,1),'r'),
            Beat(s+4.5,(1,0),'u'),
            Beat(s+5.5,(1,0),'d')]

def verse1(startBeat):
    pass

def beatMap():
    s1 = 8
    s2 = 16
    beatMap = [
        #intro section
        Beat(s1,(1,0),'r'),
        Beat(s1+2,(-1,0),'l'),
    ] + tune(24)
    return beatMap