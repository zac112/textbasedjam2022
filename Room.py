from Rooms import Rooms
from Monitor import Monitor

import GameState

class Room:
    
    def __init__(self,name):
        self.name = name
        self.menuindex = 0
        
    def postInit(self, gameState : GameState):
        self._gameState = gameState
        self._connectedRooms = []
        self._connectRooms()
        self._registerEvents()

    def enterRoom(self):
        Monitor.clear()
        self._menuitems = self._getMenuItems()
        self._registerInput(self._gameState)
        self._displayRoomDescription()
        self._displayMenuItems()
        self.__registerMenu()

    def changeRoom(self, newRoom : Rooms):
        self._unregisterInput(self._gameState)
        self.__unregisterMenu()

        if newRoom not in self._connectedRooms: raise Exception(f"Attempting to move into a not connected room from {self.name} to {newRoom}. Connected rooms are {[x.name for x in self._connectedRooms]}")        
        newRoom = self._gameState.getRoom(newRoom)
        newRoom.enterRoom()
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

    def _getActions(self) -> list:
        #Inheriting classes implement
        return []

    def __menuUp(self):
        self.menuindex = max(0, self.menuindex-1)
        Monitor.clearLines(len(self._getMenuItems())*2)        
        self._displayMenuItems()
    
    def __menuDown(self):
        self.menuindex = min(len(self._getMenuItems())-1, self.menuindex+1)
        Monitor.clearLines(len(self._getMenuItems())*2)
        self._displayMenuItems()

    def __menuAccept(self):
        pass
    
    def __registerMenu(self):
        self._gameState.registerInput(self.__menuUp, 'up')
        self._gameState.registerInput(self.__menuDown, 'down')
        self._gameState.registerInput(self.__menuAccept, 'enter')

    def __unregisterMenu(self):
        self._gameState.unregisterInput(self.__menuUp, 'up')
        self._gameState.unregisterInput(self.__menuDown, 'down')
        self._gameState.unregisterInput(self.__menuAccept, 'enter')

    def _getMenuItems(self) -> list:
        menuitems = [self._gameState.getRoom(r).getConnectionDescription() for r in self._connectedRooms]        
        menuitems.extend(self._getActions())
        return menuitems

    def _displayRoomDescription(self):
        Monitor.print(self.description, Monitor.INSTANT)

    def _displayMenuItems(self):
        for i, item in enumerate(self._getMenuItems()):
            if i==self.menuindex: item = '>'+item+'<'
            else: item = " "+item
            Monitor.print(item, Monitor.FAST)

    def getConnectionDescription(self):        
        return self.connectionDescription

class RoomPlaneCrash(Room):
        
    description = "You are at the site where you crashed your plane. Smoke is still rising from the engine"
    connectionDescription = "You see smoke rising in the distance where you crashed your plane"

    menu = {}
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.VILLAGE)

    def keypress(self):
        self.changeRoom(Rooms.VILLAGE)

class RoomVillage(Room):

    description = "You are in a small village. People are busy all around you."
    connectionDescription = "You think you see a small village some distance away"

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.PLANECRASH)
        self._connectedRooms.append(Rooms.CROSSROADS)
        self._connectedRooms.append(Rooms.CAVEENTRANCE)
        

class RoomCrossroads(Room):
    connectionDescription = "The road forks some distance away."

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.VILLAGE)
        self._connectedRooms.append(Rooms.LIGHTHOUSE)
        self._connectedRooms.append(Rooms.BEACH)

class RoomBeach(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CROSSROADS)
        self._connectedRooms.append(Rooms.CAVEENTRANCE)

class RoomCaveEntrance(Room):

    connectionDescription = "You think you see a cave entrance in the side of the mountain"

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.BEACH)
        self._connectedRooms.append(Rooms.VILLAGE)
        self._connectedRooms.append(Rooms.CAVE)

class RoomCaveExit(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVE)
        self._connectedRooms.append(Rooms.FOREST)
        self._connectedRooms.append(Rooms.CLIFFS)

class RoomCave(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEENTRANCE)
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomCliffs(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomForest(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomLighthouse(Room):
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CROSSROADS)