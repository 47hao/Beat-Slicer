from maps import VivaLaVida
from maps import TakeOnMe
from maps import BlindingLights
from maps import Radioactive

def getMap(name):
    if name == "VivaShort":
        return VivaLaVida.getData()
    elif name == "VivaLaVida":
        return VivaLaVida.getData()
    elif name == "TakeOnMe":
        return TakeOnMe.getData()
    elif name == "BlindingLights":
        return BlindingLights.getData()
    elif name == "Radioactive":
        return Radioactive.getData()
