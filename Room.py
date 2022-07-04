from Rooms import Rooms

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

    def _registerInput(self, gameState : GameState):
        #Inheriting classes implement
        pass

    def _unregisterInput(self, gameState : GameState):
        #Inheriting classes implement
        pass

    def __connectRooms(self):
        #Inheriting classes implement
        pass

class RoomPlaneCrash(Room):
        
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.VILLAGE))

    def keypress(self):
        print("Plance crash pressed")

class RoomVillage(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.PLANECRASH))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CROSSROADS))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEENTRANCE))
        

class RoomCrossroads(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.VILLAGE))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.LIGHTHOUSE))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.BEACH))

class RoomBeach(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CROSSROADS))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEENTRANCE))

class RoomCaveEntrance(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.BEACH))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.VILLAGE))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVE))

class RoomCaveExit(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVE))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.FOREST))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CLIFFS))

class RoomCave(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEENTRANCE))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEEXIT))

class RoomCliffs(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEEXIT))

class RoomForest(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEEXIT))

class RoomLighthouse(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def __connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CROSSROADS))