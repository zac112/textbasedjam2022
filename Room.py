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

    def selectFromMenu(self, fromRoom): fromRoom.changeRoom(self.room)

#region methods for subclasses
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
#endregion

#region methods for menu
    def __menuUp(self):
        self.menuindex = max(0, self.menuindex-1)
        Monitor.clearLines(len(self._getMenuItems())*2)        
        self._displayMenuItems()
    
    def __menuDown(self):
        self.menuindex = min(len(self._getMenuItems())-1, self.menuindex+1)
        Monitor.clearLines(len(self._getMenuItems())*2)
        self._displayMenuItems()

    def __menuAccept(self):
        self._getMenuItems()[self.menuindex].selectFromMenu(self)

    def __registerMenu(self):
        self._gameState.registerInput(self.__menuUp, 'up')
        self._gameState.registerInput(self.__menuDown, 'down')
        self._gameState.registerInput(self.__menuAccept, 'enter')

    def __unregisterMenu(self):
        self._gameState.unregisterInput(self.__menuUp, 'up')
        self._gameState.unregisterInput(self.__menuDown, 'down')
        self._gameState.unregisterInput(self.__menuAccept, 'enter')

    def _getMenuItems(self) -> list:
        menuitems = [self._gameState.getRoom(r) for r in self._connectedRooms]        
        menuitems.extend(self._getActions())
        return menuitems

    def _displayMenuItems(self):
        for i, item in enumerate([x.getMenuString() for x in self._getMenuItems()]):
            if i==self.menuindex: item = '>'+item+'<'
            else: item = " "+item
            Monitor.print(item, Monitor.FAST)
#endregion

    def _displayRoomDescription(self):
        Monitor.print(self.description, Monitor.INSTANT)

    def getMenuString(self):        
        return self.connectionDescription

class RoomPlaneCrash(Room):
        
    description = "You are at the site where you crashed your plane. Smoke is still rising from the engine"
    connectionDescription = "You see smoke rising in the distance where you crashed your plane"
    room = Rooms.PLANECRASH

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
    room = Rooms.VILLAGE

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

    description = "You are at a crossroads. A sign next to the road is written in a language you do not recognize"
    connectionDescription = "The road forks some distance away."
    room = Rooms.CROSSROADS

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

    description = "You find yourself on a beach. The sun shines warmly and seagulls screech occasionally."
    connectionDescription = "You see a sandy beach not far from where you are"    
    room = Rooms.BEACH

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

    description = "You end up at a large cave entrance. You see but darkness in the cave."
    connectionDescription = "You think you see a cave entrance in the side of the mountain"
    room = Rooms.CAVEENTRANCE

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

    description = "You stand next to a small cave entrance in the mountain face."
    connectionDescription = "You think you see a light up ahead"
    room = Rooms.CAVEEXIT

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

    description = "You are in a cave. After your eyes adjust to the darkness, you are able to find your way."
    connectionDescription = "Enter the cave?"
    room = Rooms.CAVE

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

    description = "You stop at a tall cliffside. Waves crash against it some hundreds of feet below you."
    connectionDescription = "You hear waves from the east"
    room = Rooms.CLIFFS

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomForest(Room):

    description = "You stand at the edge of a relatively dense forest. You see birches and other trees which you are not familiar with."
    connectionDescription = "A forest begins near you to the north."
    room = Rooms.FOREST

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomLighthouse(Room):

    description = "You stand at the bottom of a tall lighthouse."
    connectionDescription = "What looks like a tall tower looms solemnly against the horizon."
    room = Rooms.LIGHTHOUSE

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CROSSROADS)