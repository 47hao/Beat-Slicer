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
    return bpm, offset, beatMap(), fileName, 20
#=============================================================================

bpm = 136
offset = 0
fileName = "Radioactive.wav"

def beatMap():
    c1 = 68
    c2 = 100
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
        ) + [
        #dotted quarter section
        
    ]

        #Beat(c2,(2,1),'d'),
        #Beat(c2,(2,1),'u'),
        #constant beats now
    

def downUps(beat, pos, num):
    result = []
    for i in range(num):
        result.append(Beat(beat+i,pos,['d','u'][i%2]))
    return result

#syncopated rhythmic part
def syncopate(beat):
    pass