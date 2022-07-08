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
        self._gameState.registerTownAttackListener(self._getTownAttackListener())

    def reEnterRoom(self):
        if not self.roomActive :return
        self._onEnter()
        self.menuindex = 0
        self.refreshScreen()
        
    def enterRoom(self):        
        self._registerEvents()
        self._registerInput(self._gameState)
        self._registerMenu()
        self._onEnter()
        self.menuindex = 0
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
                 GameTime.DAWN:"The sun is rising",
                 GameTime.MORNING:"It's morning",
                 GameTime.NOON:"The sun is at its highest",
                 GameTime.EVENING:"It's past midday",
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

    def _getTownAttackListener(self):
        def listener(isAttacking):
            if not self.roomActive: return
            if isAttacking: Monitor.print("You have a vision of a terrible monster attacking the town.",speed=Monitor.SLOW)
            #else: Monitor.print("You see the monstrous beast flying away from the town, over the mountain.")
        return listener
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
        menuitems = []
        menuitems.extend(self._getActions())
        menuitems.extend([self._gameState.getRoom(r) for r in self._connectedRooms])        
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
        description = ""
        
        def _getConnectionString(self, fromRoom):            
            return "Examine what's left of your plane"

        def selectFromMenu(self, fromRoom : Rooms):
            if fromRoom._gameState.getTimeOfDay() == GameTime.MIDNIGHT:
                Monitor.print("It is too dark to examine the plane.")
                return
            
            fromRoom._gameState.updateKnowledge(Knowledge.ExaminedPlane)
            Monitor.print("""The damage isn't so bad as it looks.
You ruptured a fuel line and both wheels on the landing gear are destroyed.
You might be able to fix the plane given the right materials.""")            

            fromRoom._removeEvent(self)
            fromRoom.reEnterRoom()
            

    class AttachWheels(MenuItem):
        description = ""
        
        def _getConnectionString(self, fromRoom):            
            return "Attach the salvaged wheels to your plane."

        def getRequirements(self) -> list:
            return [Knowledge.CollectedWheelMaterial]
    
        def selectFromMenu(self, fromRoom : Rooms):            
            Monitor.print("""You replace your broken wheels with the ones from the biplane.
Not a perfect fit, but you should be able to take off now.""")
            
            fromRoom._gameState.updateKnowledge(Knowledge.AttachedWheel)
            if fromRoom._gameState.fulfillsRequirements([Knowledge.AddedFuelToPlane,Knowledge.AttachedFuelHose,Knowledge.AttachedWheel]):
                fromRoom._gameState.updateKnowledge(Knowledge.FixedPlane)
            
            fromRoom._gameState.removeItem(Items.Wheels)      
            fromRoom._removeEvent(self)
            fromRoom.reEnterRoom()
            
    class AddFuel(MenuItem):
        description = ""
        
        def _getConnectionString(self, fromRoom):            
            return "Add fuel to your plane"

        def getRequirements(self) -> list:
            return [Knowledge.CollectedFuelMaterial]
        
        def selectFromMenu(self, fromRoom : Rooms):
            if not fromRoom._gameState.fulfillsRequirement(Knowledge.AttachedFuelHose):
                Monitor.print("""If you add the fuel now, it would just leak to the ground.
Fix the fuel hose first.""")
                return
            fromRoom._gameState.updateKnowledge(Knowledge.AddedFuelToPlane)
            if fromRoom._gameState.fulfillsRequirements([Knowledge.AddedFuelToPlane,Knowledge.AttachedFuelHose,Knowledge.AttachedWheel]):
                fromRoom._gameState.updateKnowledge(Knowledge.FixedPlane)
                
            fromRoom._gameState.removeItem(Items.Fuel)
            Monitor.print("""You fill your plane's tank to the brim with kerosene. Luckily the fuel tank wasn't damaged.""")
            fromRoom._removeEvent(self)
            fromRoom.reEnterRoom()

    class FixHose(MenuItem):
        description = ""
        
        def _getConnectionString(self, fromRoom):            
            return "Add fuel to your plane"

        def getRequirements(self) -> list:
            return [Knowledge.FoundFuelHose]
        
        def selectFromMenu(self, fromRoom : Rooms):
            fromRoom._gameState.updateKnowledge(Knowledge.AttachedFuelHose)
            if fromRoom._gameState.fulfillsRequirements([Knowledge.AddedFuelToPlane,Knowledge.AttachedFuelHose,Knowledge.AttachedWheel]):
                fromRoom._gameState.updateKnowledge(Knowledge.FixedPlane)
                
            Monitor.print("""You jerryrig the plastic tubing to your plane. You're pretty sure that it won't leak...""")            
            fromRoom._gameState.removeItem(Items.Hose)
            fromRoom._removeEvent(self)
            fromRoom.reEnterRoom()
            

    class EscapeIsland(MenuItem):
        description = "Your plane is now fixed."
        
        def _getConnectionString(self, fromRoom):            
            return "Start the engines and escape this cursed island."

        def getRequirements(self) -> list:
            return [Knowledge.FixedPlane]
    
        def selectFromMenu(self, fromRoom : Rooms):            
            Monitor.print("""You start the plane's engine and sigh from relief when nothing exploded.""")
            Monitor.print("""You climb aboard the plane and take off.""")
            Monitor.print("""Congratulations! You have escaped the island alive!""", speed=Monitor.SLOW)
            
            fromRoom._gameState.endGame(GameEnd.WIN)
            
#endregion events
            
    descriptionIndex = 0
    description = ["You are at the site where you crashed your plane.","Smoke is still rising from the engine."]
    connectionDescription = ["You see smoke rising in the distance where you crashed your plane", "You see your plane in the distance"]
    room = Rooms.PLANECRASH    
    availableActions = [ExaminePlane()]

    def _onEnter(self):
        self.description = ["You are at the site where you crashed your plane."]
        if not self._gameState.fulfillsRequirement(Knowledge.ExaminedPlane):
            self.description.append("Smoke is still rising from the engine.")
        else:
            self.descriptionIndex = 1
        if self._gameState.fulfillsRequirement(Knowledge.ExaminedPlane):
            self.description.append("After examining the plane, you might be able to fix it.\nYou only need fuel, a length of hose and some wheels")
        
    def _getEvents(self):
        return [(self._addBirdEvent,50)]

    def _addBirdEvent(self, tick):        
        birds = self.Birds()
        self.addEvent(birds, tick+30)
        
    def _getConnectionString(self, fromRoom):
        return {Rooms.VILLAGE: self.connectionDescription[self.descriptionIndex]}[fromRoom]

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.VILLAGE)
    
class RoomVillage(Room):
#region events
    class ForceEntry(MenuItem):
        def _getConnectionString(self, fromRoom):           
            return "Ignore the men and head inside the town."

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You decide to ignore them and keep walking towards the gates. ")
            Monitor.print("The soldiers do not hesitate to impale you with their spear. You died.")
            fromRoom._gameState.endGame(GameEnd.LOSE)

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
                    GameTime.MORNING,
                    GameTime.NOON,
                    GameTime.EVENING,
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
        if self._gameState.fulfillsRequirement(Knowledge.LearnedVillageName):
            self.descriptionIndex = 2
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

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.VILLAGE)
        self._connectedRooms.append(Rooms.LIGHTHOUSE)
        self._connectedRooms.append(Rooms.BEACH)

class RoomBeach(Room):

    class Shipwreck(MenuItem):
        description = "You see pieces of debris floating on the shallows and washed ashore."
        
        def _getConnectionString(self, fromRoom):            
            return "Scavenge the flotsam"

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You begin to rummage through the debris.")
            if fromRoom._gameState.getTimeOfDay == GameTime.MIDNIGHT:
                Monitor.print('However, it is too dark to find anything.')
                return
            Monitor.print('The sun glimmers from a metallic object half-buried in the sand.')
            Monitor.print('You dig it out and find a jerry can full of kerosene!')
            fromRoom._gameState.tookAction(Actions.FoundFuel)
            fromRoom._gameState.updateKnowledge(Knowledge.CollectedFuelMaterial)
            fromRoom._gameState.addItem(Items.Fuel)
            fromRoom._removeEvent(self)
            
    descriptionIndex = 0
    description = ["You find yourself on a beach. The sun shines warmly and seagulls screech occasionally."]
    connectionDescription = ["You see a sandy beach not far from where you are"]
    room = Rooms.BEACH
    availableActions = []

    def _getConnectionString(self, fromRoom):
        return {Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CROSSROADS)
        self._connectedRooms.append(Rooms.CAVEENTRANCE)

    def shipwreck(self, ticks):
        if self._gameState.fulfillsRequirement(Knowledge.FixedLighthouse):
            Monitor.print("You hear a plane fly over the island. Maybe there is a way to force the plane to (crash?)land")
            return

        if self.roomActive:
            Monitor.print("You hear a crash and shortly thereafter flosam begins to float to the beach.")
        else:
            Monitor.print("The winds from the beach carry the sounds of a faint explosion. Maybe you imagined it.")

        self.availableActions.append(self.Shipwreck())
        

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

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEINSIDE)
        self._connectedRooms.append(Rooms.FOREST)
        self._connectedRooms.append(Rooms.CLIFFS)

class RoomCliffs(Room):

    class Shipwreck(MenuItem):
        description = "You hear creaking down the cliffside. As you peer down, you notice a biplane hanging precariously from a ledge.\nIt's not flyable anymore, but might still have usable langing gear!"
        
        def _getConnectionString(self, fromRoom):
            return "Climb down the cliffside"

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You begin to climb down the cliffside.")
            if fromRoom._gameState.getTimeOfDay == GameTime.MIDNIGHT:
                Monitor.print('However, you lose your foothold in the darkness and fall to your death.')
                fromRoom._gameState.endGame(GameEnd.LOSE)
                return
            Monitor.print('You manage to reach the plane.')
            Monitor.print('With a few good kicks, the wheels come off and you snatch them.')
            Monitor.print('You find nothing else of use and climb back up.')
            fromRoom._gameState.tookAction(Actions.ClimbedDownCliff)
            fromRoom._gameState.updateKnowledge(Knowledge.CollectedWheelMaterial)
            fromRoom._gameState.addItem(Items.Wheels)
            fromRoom._removeEvent(self)
            
    descriptionIndex = 0
    description = ["You stop at a tall cliffside. Waves crash against it some hundreds of feet below you."]
    connectionDescription = ["You hear waves from the east"]
    room = Rooms.CLIFFS
    availableActions = []

    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]}[fromRoom]

    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

    def shipwreck(self, ticks):
        if self._gameState.fulfillsRequirement(Knowledge.FixedLighthouse): return
        self.availableActions.append(self.Shipwreck())

class RoomForest(Room):

    class EnterForest(MenuItem):
        description = "You could enter the forest, but you might get lost."
        
        def _getConnectionString(self, fromRoom):
            return "Enter the forest"

        def selectFromMenu(self, fromRoom : Rooms):
            if fromRoom._gameState.hasAction(Actions.EagleQuest):
                fromRoom.changeRoom(Rooms.FORESTINSIDE)
            else:
                Monitor.print("\nYou search the forest, but don't really know what to look for.", delay=False)

    class SeekBeast(MenuItem):
        description = "In your vision, you saw the beast take flight from the forest."
        
        def _getConnectionString(self, fromRoom):
            return "Seek out the Beast"

        def selectFromMenu(self, fromRoom : Rooms):
            if fromRoom._gameState.fulfillsRequirement(Knowledge.DefeatedBeast):
                Monitor.print("You have already slain the beast; or set it free... or whatever happened")
                return
            Monitor.print("You go deep into the woods.")
            Monitor.print("Deeper than you've ever been.")
            Monitor.print("GRRWAAAAARHH",speed=Monitor.SLOW)
            Monitor.print("Uh-oh, I think you found what you were looking for.")
            if not fromRoom._gameState.hasItem(Items.SwordOfArariel):
                if fromRoom._gameState.hasItem(Items.Sword):
                    Monitor.print("You ready your rusty sword for battle with the Beast.")
                    Monitor.print("The Beast breathes fire at you; melts your sword and kills you.")
                    romRoom._gameState.endGame(GameEnd.LOSE)
                    return
                else:
                    Monitor.print("You walk up to the beast and punch it as hard as you can.")
                    Monitor.print("The Beast eats you.")
                    romRoom._gameState.endGame(GameEnd.LOSE)
                    return
            else:
                Monitor.print("The sword of Arariel begins to glow.")
                Monitor.print("The Beast breathes fire at you, but the sword deflects the Beast's magic.")
                Monitor.print("What follows is an intense battle, which I didn't have time to write for this game jam.")                
                Monitor.print("But trust me, it was an ", speed=Monitor.NORMAL, printline=False)
                Monitor.print(" epic ", speed=Monitor.SLOW, printline=False)
                Monitor.print("battle.", speed=Monitor.Normal)
                Monitor.print("Anyway,                                       ")
                Monitor.clear()
                fromRoom.changeRoom(Rooms.BEASTDIALOG)
                
                
    descriptionIndex = 0
    description = ["You stand at the edge of a relatively dense forest. You see birches and other trees which you are not familiar with."]
    connectionDescription = ["A forest begins near you to the north."]
    room = Rooms.FOREST
    availableActions = [EnterForest()]

    def _getTownAttackListener(self):
        return self.addBeastOption

    def addBeastOption(self, isAttacking):
        if not isAttacking:
            self.availableActions.append(self.SeekBeast)
        
    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]}[fromRoom]
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CAVEEXIT)

class RoomLighthouse(Room):

    class Eagle(MenuItem):
        description = "A majestic eagle has landed near the lighthouse. It looks at you with a welcoming look."
        
        def _getConnectionString(self, fromRoom):            
            return "Approach the eagle"

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("As you cautiously walk towards the eagle, you hear a soft, calming voice in your head.")
            Monitor.print('"Fear not, for I will not harm you."')
            fromRoom._gameState.tookAction(Actions.MetEagle)
            fromRoom.changeRoom(Rooms.EAGLEDIALOG)

    class FixLighthouse(MenuItem):
        description = ""
        
        def _getConnectionString(self, fromRoom):            
            return "Go light the light in the lighthouse"

        def selectFromMenu(self, fromRoom : Rooms):
            if not fromRoom._gameState.hasItem(Items.Wood):
                Monitor.print("You already lit the lighthouse's flames")                
                return
            
            Monitor.print("You find the lighthouse door unlocked and walk in.")
            Monitor.print("As you trek up numerous flights of stairs, you hope there's a way to light the magic wood you're carrying.")
            Monitor.print("... your legs begin to hurt...",speed=Monitor.SLOW)
            Monitor.print("You reach the top of the lighthouse and set the wood alight in the lamp.")
            fromRoom._gameState.updateKnowledge(Knowledge.FixedLighthouse)
            fromRoom._gameState.removeItem(Items.Wood)
            fromRoom.reEnterRoom()
            
    descriptionIndex = 0
    description = ["You stand at the bottom of a tall lighthouse."]
    connectionDescription = ["What looks like a tall tower looms solemnly against the horizon."]
    room = Rooms.LIGHTHOUSE
    availableActions = []

    def _onEnter(self):
        self.description = ["You stand at the bottom of a tall lighthouse."]
        if self._gameState.hasItem(Items.Wood):
            self.availableActions.append(self.FixLighthouse())
        if self._gameState.fulfillsRequirement(FixedLighthouse):
            self.description.append("The flames on top of the lighthouse burn brightly.")
        
        
    def _getConnectionString(self, fromRoom):
        return {Rooms.CROSSROADS: self.connectionDescription[self.descriptionIndex]}[fromRoom]
        
    def _connectRooms(self):
        self._connectedRooms.append(Rooms.CROSSROADS)

    def eagleArrives(self,tick):
        self.addEvent(self.Eagle(),tick+60)
        if self.roomActive:
            Monitor.print("An eagle lands near the lighthouse.",speed=Monitor.SLOW)
        else:
            Monitor.print("You have a vision of an eagle flying towards a lighthouse.",speed=Monitor.SLOW)

    
        
