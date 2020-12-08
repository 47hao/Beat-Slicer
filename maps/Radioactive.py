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
    return bpm, offset, beatMap(), lighting(), fileName, songName, artist, 136
#=============================================================================

bpm = 136
offset = 0
fileName = "Radioactive.wav"
songName = "Radioactive"
artist = "Imagine Dragons"

c1 = 68
c2 = 100
c3 = 132

def beatMap():
    return [
        #intro section
        Beat(12,(1,1),'d'),
        Beat(16,(-1,1),'u'),
        Beat(20,(1,1),'d'),
        Beat(24,(-1,1),'u'),
        Beat(28,(1,0),'r'),
        Beat(32,(-1,0),'l'),

        Beat(36,(2,1),'u'),
        Beat(37,(2,1),'d'),
        Beat(40,(-2,1),'u'),
        Beat(41,(-2,1),'d'),

        Beat(44,(1,1),'u'),
        Beat(45,(1,0),'d'),
        Beat(48,(-1,1),'u'),
        Beat(49,(-1,0),'d'),

        #first chorus c1=======================================
        Beat(c1,(2,0),'d'),
        #Beat(c1,(2,1),'d'),
        Beat(c1+3,(-1,-1),'l'),
        Beat(c1+4,(-2,0),'d'),
        #Beat(c1+4,(-2,1),'d'),
        
        Beat(c1+6,(1,1),'u'),

        Beat(c1+8,(-1,0),'l'),
        #Beat(c1+8,(-2,0),'l'),
        
        Beat(c1+15,(1,-1),'r'),
        Beat(c1+16,(1,-1),'l'),

        Beat(c1+18,(-1,0),'d'),
        Beat(c1+19,(1,1),'r'),
        Beat(c1+20,(1,1),'l'),

        Beat(c1+22,(-1,0),'u'),
        Beat(c1+23,(1,-1),'r'),
        Beat(c1+24,(1,-1),'l'),
        #long breath
        Beat(98,(1,0),'l'),
        Beat(98,(2,0),'l'),

        #chorus 2===================================================
    ] + ( downUps(c2, (2,1),4) + downUps(c2+4, (1,1),4) 
        + downUps(c2+8, (-1,1),4) + downUps(c2+12, (-2,1),4)
        + downUps(c2+16, (1,1),4) + downUps(c2+20, (-1,1),4)
        #dotted quarter section
        ) + [ 
        Beat(c2+24,(2,0),'r'),
        Beat(c2+28,(-2,0),'l')
    ] + [
        Beat(c3,(2,1),'d')
    ] + c3Pattern(c3) + c3Pattern(c3+8) + [
        #chorus 3===================================================
    ]

def c3Pattern(s):
    return [
        Beat(s+2,(2,0),'u'),
        
        Beat(s+3,(1,-1),'l'),
        Beat(s+3,(-1,-1),'l'),
        Beat(s+4,(-2,1),'d'),
    
        Beat(s+6,(-2,0),'u'),
        
        Beat(s+7,(-1,-1),'r'),
        Beat(s+7,(1,-1),'r'),
        Beat(s+8,(2,1),'d'),
    ]

def lighting():
    return introDrumLighting(c1) + introDrumLighting(c2)

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

def downUps(beat, pos, num):
    result = []
    for i in range(num):
        result.append(Beat(beat+i,pos,['d','u'][i%2]))
    return result

#syncopated rhythmic part
def syncopate(beat):
    pass