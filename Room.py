import GameState

class Room:

    _connectedRooms = []
    
    def __init__(self,name):
        self.name = name
        
    def postInit(self, gameState : GameState):
        self._gameState = gameState
        self.__connectRooms()

    def enterRoom(self):
        self.registerInput(self._gameState)

    def changeRoom(self, newRoom):
        self.unregisterInput(self._gameState)
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
        self._connectedRooms.append(self._gameState.getRoom("Village"))

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