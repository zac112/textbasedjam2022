from Monitor import Monitor
from MenuItem import MenuItem
from Enums import *

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

    def reEnterRoom(self):
        if not self.roomActive :return
        self._onEnter()        
        self.refreshScreen()
        
    def enterRoom(self):        
        self._registerEvents()
        self._registerInput(self._gameState)
        self._registerMenu()
        self._onEnter()
        self.roomActive = True
        self.refreshScreen()

    def changeRoom(self, newRoom : Rooms):
        self._unregisterInput(self._gameState)
        self._unregisterMenu()
        self._unregisterEvents()
        self._onExit()
        self.roomActive = False        
        
        newRoom = self._gameState.getRoom(newRoom)
        newRoom.enterRoom()
        return newRoom

    def refreshScreen(self):
        if not self.roomActive :return
        
        Monitor.clear()        
        self._displayApproximateTime()
        self._displayRoomDescription()
        self.menupos = Monitor.getCursorPos()
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
        if not self._shouldDisplayApproximateTime(): return
        
        texts = {GameTime.MIDNIGHT:"It's very dark",
                 GameTime.DAWN:"Sun is rising",
                 GameTime.NOON:"The sun is at its highest",
                 GameTime.DUSK:"The sun is setting"}
        time = self._gameState.getTime()[1]
        Monitor.print(texts[time], delay=False)

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
    
    def _onExit(self):
        #Inheriting classes implement
        pass

    def _getEvents(self):
        #Inheriting classes implement
        return []
    
    def _getConnectionString(self) -> dict:
        #Inheriting classes implement
        return {}

    def _shouldDisplayApproximateTime(self):
        return True

    def getGlobalEvents(self):
        #Inheriting classes implement
        #Global events are important plot points that happen regardless of player involvement
        #list[(method,tick)]
        return []
#endregion

#region methods for menu
    def _menuUp(self):
        self.menuindex = max(0, self.menuindex-1)      
        self._displayMenuItems()
    
    def _menuDown(self):
        self.menuindex = min(len(self._getMenuItems())-1, self.menuindex+1)
        self._displayMenuItems()

    def _menuAccept(self):
        self._getMenuItems()[self.menuindex].selectFromMenu(self)

    def _registerMenu(self):
        self._gameState.registerInput(self._menuUp, 'up')
        self._gameState.registerInput(self._menuDown, 'down')
        self._gameState.registerInput(self._menuAccept, 'enter')

    def _unregisterMenu(self):
        self._gameState.unregisterInput(self._menuUp, 'up')
        self._gameState.unregisterInput(self._menuDown, 'down')
        self._gameState.unregisterInput(self._menuAccept, 'enter')

    def _getMenuItems(self) -> list:
        menuitems = [self._gameState.getRoom(r) for r in self._connectedRooms]        
        menuitems.extend(self._getActions())
        return menuitems

    def _displayMenuItems(self):
        Monitor.setCursorPos(self.menupos)
        for i, item in enumerate([self._getMenuString(x) for x in self._getMenuItems()]):        
            if i==self.menuindex: item = '>'+item+'<'
            else: item = " "+item+" "
            Monitor.print(item, speed=Monitor.FAST, delay=False)
#endregion

    def _displayRoomDescription(self):
        for line in self.description:
            Monitor.print(line, delay=False)
        Monitor.printLine()

    def _getMenuString(self, item):        
        return item._getConnectionString(self.room)

    def addEvent(self, event, endtick):
        self.availableActions.append(event)
        self._gameState.registerEvent(lambda a:self._removeEvent(event),endtick)  
        self.description.append(event.description)
        self.refreshScreen()

    def _removeEvent(self,event):
        self.availableActions = [x for x in self.availableActions if x != event]        
        try:
            self.description.remove(event.description)
            self._menuUp()
            self.refreshScreen()
        except: pass
        
        
class RoomPlaneCrash(Room):    

#region events
    class Birds(MenuItem):
        description = "Some birds have flown in to sit on your plane"
        
        def _getConnectionString(self, fromRoom):            
            return "Chase the birds"

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You chase the birds away")
            fromRoom._gameState.tookAction(Actions.ChasedBirds)
            fromRoom._removeEvent(self)

    class ExaminePlane(MenuItem):
        description = "After examining the plane, you might be able to fix it.\nYou only need fuel, a length of hose and some wheels"
        
        def _getConnectionString(self, fromRoom):            
            return "Examine what's left of your plane"

        def selectFromMenu(self, fromRoom : Rooms):
            if fromRoom._gameState.getTimeOfDay == GameTime.MIDNIGHT:
                Monitor.print("It is too dark to examine the plane.")
                return
            
            fromRoom._gameState.updateKnowledge(Knowledge.ExaminedPlane)
            Monitor.print("""The damage isn't so bad as it looks.
You ruptured a fuel line and both wheels on the landing gear are destroyed.
You might be able to fix the plane given the right materials.""")
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
        return [(self._addBirdEvent,50)]

    def _addBirdEvent(self, tick):        
        birds = self.Birds()
        self.addEvent(birds, tick+30)
        
    def _getConnectionString(self, fromRoom):
        return {Rooms.VILLAGE: self.connectionDescription[self.descriptionIndex]}[fromRoom]

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
        def _getConnectionString(self, fromRoom):           
            return "Ignore the men and head inside the town."

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You decide to ignore them and keep walking towards the gates. ")
            Monitor.print("The soldiers do not hesitate to impale you with their spear. You died.")
            fromRoom._gameState.endGame()

        def getAllowedTimes(self) -> list:
            return [GameTime.MIDNIGHT]

    class VillageInside(MenuItem):
        def _getConnectionString(self, fromRoom):            
            return "Head inside the town."

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You enter the village")            
            fromRoom.changeRoom(Rooms.VILLAGEINSIDE)

        def getAllowedTimes(self) -> list:
            return [GameTime.DUSK,
                    GameTime.NOON,
                    GameTime.DAWN]
#endregion events
            
    descriptionIndex = 0
    description = ["You reach a small walled town."]
    connectionDescription = ["You think you see a small village some distance away", "You see the village some distance away", "You see Thurstan some distance away"]
    room = Rooms.VILLAGE
    availableActions = []
    
    def _onEnter(self):
        self.availableActions = []
        self.description = ["You reach a small walled town."]
        self._gameState.updateKnowledge(Knowledge.VisitedVillage)
        self.descriptionIndex = 1        
        if self._gameState.getTimeOfDay()==GameTime.MIDNIGHT:
            self.description[0]+=" The gates are closed."
            dialog = {True:"They say entry is not allowed at night",
                      False:"They speak a language unknown to you."}
            self.description.append("You are stopped at the gates by two men armed with spears. \n"+dialog[self._gameState.fulfillsRequirement(Knowledge.LearnedLanguage)])
            self.availableActions.append(self.ForceEntry())
            return
        self.description[0]+=" The gates are open."
        self.availableActions.append(self.VillageInside())

    def _getConnectionString(self, fromRoom):
        return {Rooms.PLANECRASH: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]

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
    
    def _getConnectionString(self, fromRoom):
        return {Rooms.VILLAGE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.LIGHTHOUSE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.BEACH: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]
    
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

    def _getConnectionString(self, fromRoom):
        return {Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]

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

    def _getConnectionString(self, fromRoom):
        return {Rooms.BEACH: self.connectionDescription[self.descriptionIndex]
                ,Rooms.VILLAGE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEINSIDE: self.connectionDescription[1]
                }[fromRoom]

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.BEACH)
        self._connectedRooms.append(Rooms.VILLAGE)
        self._connectedRooms.append(Rooms.CAVEINSIDE)

class RoomCaveExit(Room):

    descriptionIndex = 0
    description = ["You stand next to a small cave entrance in the mountain face."]
    connectionDescription = ["You can head down the road that will lead you back to the cave.","You think you see a light up ahead"]
    room = Rooms.CAVEEXIT
    availableActions = []

    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEINSIDE: self.connectionDescription[1]
                ,Rooms.FOREST: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CLIFFS: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEINSIDE)
        self._connectedRooms.append(Rooms.FOREST)
        self._connectedRooms.append(Rooms.CLIFFS)

class RoomCliffs(Room):

    descriptionIndex = 0
    description = ["You stop at a tall cliffside. Waves crash against it some hundreds of feet below you."]
    connectionDescription = ["You hear waves from the east"]
    room = Rooms.CLIFFS
    availableActions = []

    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]}[fromRoom]

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

    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]}[fromRoom]

    def _registerInput(self):
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

    def _getConnectionString(self, fromRoom):
        return {Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]}[fromRoom]

    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.keypress, "k")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.keypress, "k")

    def keypress(self):
        print("Village pressed")
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CROSSROADS)

    def getGlobalEvents(self):
        return [(self.eagleArrives,180)]

    def eagleArrives(self,tick):
        if self.roomActive:
            Monitor.print("An eagle lands near the lighthouse.",speed=Monitor.SLOW)
        else:
            Monitor.print("You have a vision of an eagle flying towards a lighthouse.",speed=Monitor.SLOW)
