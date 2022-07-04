import GameState
import Rooms

class Room:

    _connectedRooms = []
    
    def __init__(self,name):
        self.name = name
        
    def postInit(self, gameState : GameState):
        self.gameState = gameState
        self.__connectRooms()

    def enterRoom(self):
        self.registerInput(self.gameState)

    def changeRoom(self, newRoom):
        self.unregisterInput(self.gameState)
        newRoom.enterRoom()
        return newRoom

    def registerInput(self, gameState : GameState):
        #Inheriting classes implement
        pass

    def unregisterInput(self, gameState : GameState):
        #Inheriting classes implement
        pass

    def __connectRooms(self):
        #Inheriting classes implement
        pass

class RoomPlaneCrash(Room):
        
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Plance crash pressed")

    def __connectRooms(self):
        self._connectedRooms.append(Rooms.VILLAGE)

class RoomVillage(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(Rooms.PLANECRASH)
        

class RoomCrossroads(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        print("Room methods call")

class RoomBeach(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        print("Room methods call")
class RoomCaveEntrance(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        print("Room methods call")

class RoomCaveExit(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        print("Room methods call")

class RoomCave(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        print("Room methods call")

class RoomCliffs(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        print("Room methods call")

class RoomForest(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def __connectRooms(self):
        print("Room methods call")

class RoomLighthouse(Room):
    def registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def __connectRooms(self):
        print("Room methods call")