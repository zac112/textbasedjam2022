from Rooms import Rooms
from Monitor import Monitor

import GameState

class Room:

    _connectedRooms = []
    
    def __init__(self,name):
        self.name = name
        
    def postInit(self, gameState : GameState):
        self._gameState = gameState
        self._connectRooms()

    def enterRoom(self):
        print("fsd")
        self._registerInput(self._gameState)
        self._displayRoomDescription()

    def changeRoom(self, newRoom : Rooms):
        self._unregisterInput(self._gameState)
        if newRoom not in self._connectedRooms: raise Exception(f"Attempting to move into a not connected room from {self.name} to {newRoom}")
        self._gameState.getRoom(newRoom).enterRoom()
        return newRoom

    def _registerInput(self, gameState : GameState):
        #Inheriting classes implement
        pass

    def _unregisterInput(self, gameState : GameState):
        #Inheriting classes implement
        pass

    def _connectRooms(self):
        #Inheriting classes implement
        pass

    def _registerEvents(self):
        #Inheriting classes implement
        pass

    def _displayRoomDescription(self):
        #Inheriting classes implement
        raise Exception(f"{self.name} does not have a description")

class RoomPlaneCrash(Room):
        
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def _connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.VILLAGE))

    def keypress(self):
        print("Plance crash pressed")

    def _displayRoomDescription(self):
        Monitor.print("You see a crashed plane.")

class RoomVillage(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
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

    def _connectRooms(self):
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

    def _connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CROSSROADS))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEENTRANCE))

class RoomCaveEntrance(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
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

    def _connectRooms(self):
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

    def _connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEENTRANCE))
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEEXIT))

class RoomCliffs(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEEXIT))

class RoomForest(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CAVEEXIT))

class RoomLighthouse(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(self._gameState.getRoom(Rooms.CROSSROADS))