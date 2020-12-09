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
    return bpm, offset, beatMap(), lighting(), fileName, songName, artist, 0
#=============================================================================

bpm = 86
offset = -0.1
fileName = "BlindingLights.wav"
songName = "Blinding Lights"
artist = "The Weeknd"

s = 10
def beatMap():
    return [
        Beat(s,(2,-1),'r'),
        Beat(s+1,(-2,-1),'l'),
        Beat(s+2,(2,-1),'r'),

        Beat(s+2.5,(2,1),'d'),
        Beat(s+3,(2,0),'u'),

        Beat(s+4,(-2,-1),'l'),
        Beat(s+5,(2,-1),'r'),
        Beat(s+6,(-2,-1),'l'),
        
        Beat(s+6.5,(-2,1),'d'),
        Beat(s+7,(-2,0),'u'),
        
        Beat(s+8,(-1,0),'r'),
        Beat(s+8,(1,0),'r'),
        Beat(s+10,(-1,0),'l'),
        Beat(s+10,(1,0),'l'),

        Beat(s+12,(2,-1),'r'),
        Beat(s+13,(2,-1),'l'),
        Beat(s+14,(2,-1),'r'),
        Beat(s+15,(2,-1),'l'),

        Beat(s+16.5,(-2,0),'d'),
        Beat(s+17.5,(-2,0),'u'),
        Beat(s+18.5,(-2,0),'d'),
        Beat(s+19.5,(-2,0),'u'),
        Beat(s+20.5,(2,0),'d'),
        Beat(s+21.5,(2,0),'u'),
        Beat(s+22.5,(2,0),'d'),
        Beat(s+23.5,(2,0),'u'),

        Beat(s+24,(1,-1),'r'),
        Beat(s+24,(2,-1),'r'),
        Beat(s+26,(-1,-1),'l'),
        Beat(s+26,(-2,-1),'l'),
        Beat(s+28,(1,0),'d'),

    ]


def lighting():
    return ([i for i in range(s,s+10,4)] + [s+10,s+12] + 
            [i for i in range(s+16,s+21,4)] + [s+24,s+26])

def introDrumLighting(s):
    return [
        i for i in range(s,s+10,4)
    ] + [
        i for i in range(s+3,s+10,4)
    ] + [s+12] + [
        i for i in range(s+15,s+25,4)
    ] + [
        i for i in range(s+16,s+25,4)
    ]


#syncopated rhythmic part
def syncopate(beat):
    pass