from Knowledge import Knowledge
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
        self._displayApproximateTime()
        self._displayMenuItems()
        self.__registerMenu()        
        self._onEnter()

    def changeRoom(self, newRoom : Rooms):
        self._unregisterInput(self._gameState)
        self.__unregisterMenu()

        if newRoom not in self._connectedRooms: raise Exception(f"Attempting to move into a not connected room from {self.name} to {newRoom}. Connected rooms are {[x.name for x in self._connectedRooms]}")        
        newRoom = self._gameState.getRoom(newRoom)
        newRoom.enterRoom()
        return newRoom

    def selectFromMenu(self, fromRoom): fromRoom.changeRoom(self.room)

    def _registerEvents(self):
        for e in self._events:
            obs, tick = e
            self._gameState.registerEvent(obs,tick)
        
    def _displayApproximateTime(self):
        tick = self._gameState.getTick()
        day = int(tick/360.0)+1
        tick = tick%360
        texts = [(60,"It's very dark"),
                 (120,"Sun is rising"),
                 (180,"The sun is at its highest"),
                 (240,"The sun is setting"),
                 (360,"It's very dark")]

        Monitor.print([t[1] for t in texts if tick<t[0]][0])   
        
            
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

    def _onEnter(self):
        #Inheriting classes implement
        pass

    def _getActions(self) -> list:
        #Inheriting classes implement
        return []
    
    def _getConnectionStrings(self) -> dict:
        #Inheriting classes implement
        return {}
#endregion

#region methods for menu
    def __menuUp(self):
        self.menuindex = max(0, self.menuindex-1)
        Monitor.clearLines(len(self._getMenuItems()))        
        self._displayMenuItems()
    
    def __menuDown(self):
        self.menuindex = min(len(self._getMenuItems())-1, self.menuindex+1)
        Monitor.clearLines(len(self._getMenuItems()))
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
        for i, item in enumerate([x.getMenuString(self.room) for x in self._getMenuItems()]):
            if i==self.menuindex: item = '>'+item+'<'
            else: item = " "+item
            Monitor.print(item, Monitor.FAST)
#endregion

    def _displayRoomDescription(self):
        Monitor.print(self.description, Monitor.INSTANT)
        Monitor.printLine()

    def getMenuString(self, room):  
        return self._getConnectionStrings()[room]

class RoomPlaneCrash(Room):
    
    descriptionIndex = 0
    description = "You are at the site where you crashed your plane. Smoke is still rising from the engine"
    connectionDescription = ["You see smoke rising in the distance where you crashed your plane", "You see your plane in the distance"]
    room = Rooms.PLANECRASH
    _events = []
    
    def _getConnectionStrings(self):
        return {Rooms.VILLAGE: self.connectionDescription[self.descriptionIndex]}

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.VILLAGE)

    def keypress(self):
        self.changeRoom(Rooms.VILLAGE)

class RoomVillage(Room):

    descriptionIndex = 0
    description = "You are in a small village. People are busy all around you."
    connectionDescription = ["You think you see a small village some distance away", "You see the village some distance away", "You see Thurstan some distance away"]
    room = Rooms.VILLAGE
    _events = []
    
    def _onEnter(self):
        self._gameState.updateKnowledge(Knowledge.VisitedVillage)
        self.descriptionIndex = 1
        

    def _getConnectionStrings(self):
        return {Rooms.PLANECRASH: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                }

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

    descriptionIndex = 0
    description = "You are at a crossroads. A sign next to the road is written in a language you do not recognize"
    connectionDescription = ["The road forks some distance away."]
    room = Rooms.CROSSROADS
    _events = []
    
    def _getConnectionStrings(self):
        return {Rooms.VILLAGE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.LIGHTHOUSE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.BEACH: self.connectionDescription[self.descriptionIndex]
                }
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

    descriptionIndex = 0
    description = "You find yourself on a beach. The sun shines warmly and seagulls screech occasionally."
    connectionDescription = ["You see a sandy beach not far from where you are"]
    room = Rooms.BEACH
    _events = []

    def _getConnectionStrings(self):
        return {Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                }  

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

    descriptionIndex = 0
    description = "You end up at a large cave entrance. You see but darkness in the cave."
    connectionDescription = ["You think you see a cave entrance in the side of the mountain", "You can head down a corridor which you think takes you back to the village"]
    room = Rooms.CAVEENTRANCE
    _events = []

    def _getConnectionStrings(self):
        return {Rooms.BEACH: self.connectionDescription[self.descriptionIndex]
                ,Rooms.VILLAGE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVE: self.connectionDescription[1]
                }

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

    descriptionIndex = 0
    description = "You stand next to a small cave entrance in the mountain face."
    connectionDescription = ["You can head down the road that will lead you back to the cave.","You think you see a light up ahead"]
    room = Rooms.CAVEEXIT
    _events = []

    def _getConnectionStrings(self):
        return {Rooms.CAVE: self.connectionDescription[1]
                ,Rooms.FOREST: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CLIFFS: self.connectionDescription[self.descriptionIndex]
                }

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

    descriptionIndex = 0
    description = "You are in a cave. After your eyes adjust to the darkness, you are able to find your way."
    connectionDescription = ["Enter the cave?"]
    room = Rooms.CAVE
    _events = []

    def _getConnectionStrings(self):
        return {Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]
                }

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

    descriptionIndex = 0
    description = "You stop at a tall cliffside. Waves crash against it some hundreds of feet below you."
    connectionDescription = ["You hear waves from the east"]
    room = Rooms.CLIFFS
    _events = []

    def _getConnectionStrings(self):
        return {Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]}

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomForest(Room):

    descriptionIndex = 0
    description = "You stand at the edge of a relatively dense forest. You see birches and other trees which you are not familiar with."
    connectionDescription = ["A forest begins near you to the north."]
    room = Rooms.FOREST
    _events = []

    def _getConnectionStrings(self):
        return {Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]}

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomLighthouse(Room):

    descriptionIndex = 0
    description = "You stand at the bottom of a tall lighthouse."
    connectionDescription = ["What looks like a tall tower looms solemnly against the horizon."]
    room = Rooms.LIGHTHOUSE
    _events = []

    def _getConnectionStrings(self):
        return {Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]}

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CROSSROADS)
