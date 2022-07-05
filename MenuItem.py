from Monitor import Monitor
from Rooms import *

class MenuItem:

    description = "Not implemented"
        
    def getMenuString(self, room : Rooms):            
        raise Exception("Menu selection not implemented")

    def selectFromMenu(self, fromRoom : Rooms):
        raise Exception("Menu selection not implemented")

    def getRequirements(self) -> list:
        return []
