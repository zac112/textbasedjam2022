from Knowledge import Knowledge
from Rooms import Rooms
from Monitor import Monitor
from MenuItem import MenuItem
from GameTime import GameTime

import GameState

class Room:
    
    def __init__(self,name):
        self.name = name
        self.menuindex = 0
        
    def postInit(self, gameState : GameState):
        self._gameState = gameState
        self._connectedRooms = []
        self._connectRooms()        
        self.roomActive = False

    def enterRoom(self):             
        self._registerEvents()
        self._registerInput(self._gameState)
        self._onEnter()
        self.refreshScreen()
        self.__registerMenu()                
        self.roomActive = True

    def changeRoom(self, newRoom : Rooms):
        self._unregisterInput(self._gameState)
        self.__unregisterMenu()
        self._unregisterEvents()
        self.roomActive = False
        
        if newRoom not in self._connectedRooms: raise Exception(f"Attempting to move into a not connected room from {self.name} to {newRoom}. Connected rooms are {[x.name for x in self._connectedRooms]}")        
        newRoom = self._gameState.getRoom(newRoom)
        newRoom.enterRoom()
        return newRoom

    def refreshScreen(self):
        Monitor.clear()
        self._displayRoomDescription()
        self._displayApproximateTime()
        self.menux, self.menuy = Monitor.getCursorPos()
        self._displayMenuItems()
        
    def selectFromMenu(self, fromRoom): fromRoom.changeRoom(self.room)

    def _registerEvents(self):        
        for e in self._getEvents():
            (obs, tick) = e
            self._gameState.registerEvent(obs,tick)

    def _unregisterEvents(self):        
        for e in self._getEvents():
            (obs, tick) = e
            self._gameState.unregisterEvent(obs,tick)

    def _displayApproximateTime(self):
        texts = {GameTime.MIDNIGHT:"It's very dark",
                 GameTime.DAWN:"Sun is rising",
                 GameTime.NOON:"The sun is at its highest",
                 GameTime.DUSK:"The sun is setting"}
        time = self._gameState.getTime()[1]
        Monitor.print(texts[time])

    def _getActions(self) -> list:
        actions = []
        for action in self.availableActions:
            reqs = map(lambda a: self._gameState.fulfillsRequirement(a), action.getRequirements())
            if not all(reqs): continue
            if self._gameState.getTimeOfDay() not in action.getAllowedTimes(): continue
            actions.append(action)
            
        return actions
    
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

    def _getEvents(self):
        #Inheriting classes implement
        return []
    
    def _getConnectionStrings(self) -> dict:
        #Inheriting classes implement
        return {}
#endregion

#region methods for menu
    def __menuUp(self):
        self.menuindex = max(0, self.menuindex-1)      
        self._displayMenuItems()
    
    def __menuDown(self):
        self.menuindex = min(len(self._getMenuItems())-1, self.menuindex+1)
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
        Monitor.setCursorPos(self.menux,self.menuy)
        for i, item in enumerate([x.getMenuString(self.room) for x in self._getMenuItems()]):
            if i==self.menuindex: item = '>'+item+'<'
            else: item = " "+item+" "
            Monitor.print(item, speed=Monitor.FAST)
#endregion

    def _displayRoomDescription(self):
        for line in self.description:
            Monitor.print(line)
        Monitor.printLine()

    def getMenuString(self, room : Rooms):  
        return self._getConnectionStrings()[room]

    def addEvent(self, event, endtick):
        self.availableActions.append(event)
        self._gameState.registerEvent(lambda a:self._removeEvent(event),endtick)  
        self.description.append(event.description)
        self.refreshScreen()

    def _removeEvent(self,event):
        self.availableActions = [x for x in self.availableActions if x != event]        
        try:
            self.description.remove(event.description)
            self.__menuUp()
            self.refreshScreen()
        except: pass
        
        
class RoomPlaneCrash(Room):    

#region events
    class Birds(MenuItem):
        description = "Some birds have flown in to sit on your plane"
        
        def getMenuString(self, room : Rooms):            
            return "Chase the birds"

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You chase the birds away", delay=1)
            fromRoom._removeEvent(self)

    class ExaminePlane(MenuItem):
        description = "After examining the plane, you might be able to fix it.\nYou only need fuel, a length of hose and some wheels"
        
        def getMenuString(self, room : Rooms):            
            return "Examine what's left of your plane"

        def selectFromMenu(self, fromRoom : Rooms):
            fromRoom._gameState.updateKnowledge(Knowledge.ExaminedPlane)
            Monitor.print("""The damage isn't so bad as it looks.
You ruptured a fuel line and both wheels on the landing gear are destroyed.
You might be able to fix the plane given the right materials.""", delay=3)
            if self.description not in fromRoom.description :
                fromRoom.description.append(self.description)
            fromRoom.refreshScreen()

#endregion events
            
    descriptionIndex = 0
    description = ["You are at the site where you crashed your plane. Smoke is still rising from the engine."]
    connectionDescription = ["You see smoke rising in the distance where you crashed your plane", "You see your plane in the distance"]
    room = Rooms.PLANECRASH    
    availableActions = [ExaminePlane()]
    
    def _getEvents(self):
        return [(self.__addBirdEvent,5)]

    def __addBirdEvent(self, tick):        
        birds = self.Birds()
        self.addEvent(birds, tick+30)
        
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
#region events
    class ForceEntry(MenuItem):
        def getMenuString(self, room : Rooms):            
            return "Ignore the men and head inside the town."

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You decide to ignore them and keep walking towards the gates. ", delay=1)
            Monitor.print("The soldiers do not hesitate to impale you with their spear. You died.", delay=1)
            fromRoom._gameState.endGame()

        def getAllowedTimes(self) -> list:
            return [GameTime.MIDNIGHT]
    
#endregion events
            
    descriptionIndex = 0
    description = ["You reach a small walled town."]
    connectionDescription = ["You think you see a small village some distance away", "You see the village some distance away", "You see Thurstan some distance away"]
    room = Rooms.VILLAGE
    availableActions = []
    
    def _onEnter(self):
        availableActions = []
        self.description = ["You reach a small walled town."]
        self._gameState.updateKnowledge(Knowledge.VisitedVillage)
        self.descriptionIndex = 1
        print(self._gameState.getTimeOfDay())
        if self._gameState.getTimeOfDay()==GameTime.MIDNIGHT:
            self.description.append("You are stopped at the gates by two men armed with spears. \nThey speak a language unknown to you.")
            self.availableActions.append(self.ForceEntry())
        

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
        print(Monitor.cursorPos())

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.PLANECRASH)
        self._connectedRooms.append(Rooms.CROSSROADS)
        self._connectedRooms.append(Rooms.CAVEENTRANCE)
        

class RoomCrossroads(Room):

    descriptionIndex = 0
    description = ["You are at a crossroads. A sign next to the road is written in a language you do not recognize"]
    connectionDescription = ["The road forks some distance away."]
    room = Rooms.CROSSROADS
    availableActions = []
    
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
    description = ["You find yourself on a beach. The sun shines warmly and seagulls screech occasionally."]
    connectionDescription = ["You see a sandy beach not far from where you are"]
    room = Rooms.BEACH
    availableActions = []

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
    description = ["You end up at a large cave entrance. You see but darkness in the cave."]
    connectionDescription = ["You think you see a cave entrance in the side of the mountain", "You can head down a corridor which you think takes you back to the village"]
    room = Rooms.CAVEENTRANCE
    availableActions = []

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
    description = ["You stand next to a small cave entrance in the mountain face."]
    connectionDescription = ["You can head down the road that will lead you back to the cave.","You think you see a light up ahead"]
    room = Rooms.CAVEEXIT
    availableActions = []

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
    description = ["You are in a cave. After your eyes adjust to the darkness, you are able to find your way."]
    connectionDescription = ["Enter the cave?"]
    room = Rooms.CAVE
    availableActions = []

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
    description = ["You stop at a tall cliffside. Waves crash against it some hundreds of feet below you."]
    connectionDescription = ["You hear waves from the east"]
    room = Rooms.CLIFFS
    availableActions = []

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
    description = ["You stand at the edge of a relatively dense forest. You see birches and other trees which you are not familiar with."]
    connectionDescription = ["A forest begins near you to the north."]
    room = Rooms.FOREST
    availableActions = []

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
    description = ["You stand at the bottom of a tall lighthouse."]
    connectionDescription = ["What looks like a tall tower looms solemnly against the horizon."]
    room = Rooms.LIGHTHOUSE
    availableActions = []

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
