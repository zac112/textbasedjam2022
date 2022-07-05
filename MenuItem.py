from Monitor import Monitor
from Rooms import *
from GameTime import GameTime

class MenuItem:

    description = "Not implemented"
        
    def getMenuString(self, room : Rooms):            
        raise Exception("Menu selection not implemented")

    def selectFromMenu(self, fromRoom : Rooms):
        raise Exception("Menu selection not implemented")

    def getRequirements(self) -> list:
        return []

    def getAllowedTimes(self) -> list:
        return [GameTime.MIDNIGHT,
                GameTime.DAWN,
                GameTime.NOON,
                GameTime.DUSK]
