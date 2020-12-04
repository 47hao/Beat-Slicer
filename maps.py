from maps import VivaLaVida

def getMap(name):
    if name == "VivaShort":
        return (VivaLaVida.bpm, VivaLaVida.delay, 
                VivaLaVida.beatMap(), "VivaShort.mp4")
    elif name == "VivaLaVida":
        pass