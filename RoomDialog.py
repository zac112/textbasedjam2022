from Monitor import Monitor
from MenuItem import MenuItem
from Room import Room
from Enums import *

class RoomDialog(Room):
    def _getMenuItems(self) -> list:
        return list(self.dialog[-1][1].keys())

    def _getMenuString(self, item):
        return item
    
    def _menuAccept(self):                
        self.dialog[-1][1][self._getMenuItems()[self.menuindex]]()
        self.description,dialog = self.dialog[-1]
        self.refreshScreen()

    def _advanceDialog(self, nextDialog):
        Monitor.clear()
        if nextDialog: self.dialog.append(nextDialog)
        else: self.dialog.pop()
        self.refreshScreen()

    def _shouldDisplayApproximateTime(self):
        return False
        
class RoomCastleInside(RoomDialog):

    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.LABORATORYINSIDE
    availableActions = []

    def _getTownAttackListener(self):
        return lambda isAttacked: self.theBeastAttacks() if isAttacked else self.theBeastLeaves()
    
    def _onEnter(self):
        if self.underAttack:
            Monitor.print("There is nobody here; they're all fighting outside!")
            self.exitRoom()
            return
        
        self.description = ["You enter a huge castle in this small village. You see a royal figure sitting on a throne."]
        self.dialog = []
        kingDialogLang = {True:": Who are you?",
                          False:", but you do not understand him."}
        kingDialog = (["The king talks with a booming voice"+kingDialogLang[self._gameState.fulfillsRequirement(Knowledge.LearnedLanguage)]],
                      {"Answer":lambda:self.answerKing(None)})
        menuOptions={
            'Talk to King':lambda:self.talkToKing(kingDialog),
            'Exit': self.exitRoom
        }            
        self.dialog.append((self.description,menuOptions))
        Monitor.clear()

    def answerKing(self, nextDialog):
        self.description[0] = "You try to answer the king, but can not say a word."
        self._advanceDialog(nextDialog)
        
    def talkToKing(self, nextDialog):
        self._advanceDialog(nextDialog)
        
    def exitRoom(self):
        self.changeRoom(Rooms.VILLAGEINSIDE)

    def theBeastAttacks(self):
        self.underAttack = True

    def theBeastLeaves(self):
        self.underAttack = False
        
class RoomLaboratoryInside(RoomDialog):
    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.LABORATORYINSIDE
    availableActions = []
    
    def _onEnter(self):
        if self._gameState.fulfillsRequirement(Knowledge.LearnedLanguage):
            Monitor.print("You think about entering the room with the machine. You decide against it.")
            self.exitRoom()
            return
            
        self.description = ["You enter what seems to be a laboratory.\You see a giant machine with three buttons on it.\nYou also notice some frescos on the walls."]
        self.dialog = []
        machineDialog = (["Which button do you press?"],
                      {"RED!":lambda:self.buttonPress(None, self.redButton)(),
                       "YELLOW!":lambda:self.buttonPress(None,self.yellowButton)(),
                       "BLUE!":lambda:self.buttonPress(None,self.blueButton)(),
                       "Let me think about this...":lambda:self._advanceDialog(None)})

        frescoDialog = (["""You see three frescos on the walls.
One has a yellow cloaked figure talking to a group of people.
The second is a depiction of a sunset over a strikingly blue ocean, with something in the sky. Could be a bird or just a smudge.
The third one depicts a battlefield with a two-headed figure in red armor victoriously poised over the corpse of a horrendous beast."""],
                      {"Stop looking at the frescos":lambda:self._advanceDialog(None)})

        menuOptions={
            'Push a button on the machine':lambda:self._advanceDialog(machineDialog),
            'Look at the frescos':lambda:self._advanceDialog(frescoDialog),
            'Exit': self.exitRoom
        }            
        self.dialog.append((self.description,menuOptions))
        Monitor.clear()

    def buttonPress(self, nextDialog, method):
        def a():
            method()
            Monitor.print("Several scientists (presumably) barge in the room and begin questioning you.")
            Monitor.print("To your great surprise, you undestand these people and are able to talk your way out of being thrown in jail.")
            self._gameState.updateKnowledge(Knowledge.LearnedLanguage)
            self.exitRoom()
        return a
    
    def redButton(self):
        Monitor.print("You press the red button and the machine whirrs to life.")
        Monitor.print("WHRR R R GZZGZZ (BLUB BLUB BLUB BLUB)",speed=Monitor.SLOW)
        Monitor.print("You grab the bottle of blood-like liquid produced by the machine and chug it in one go.")
        self._gameState.tookAction(Actions.RedPotion)
        
    def yellowButton(self):
        Monitor.print("You press the yellow button and the machine whirrs to life.")
        Monitor.print("CHUGCHUG CHCH CGCGCGCG (BLUB BLUB BLUB BLUB)",speed=Monitor.SLOW )
        Monitor.print("You grab the bottle of almost transparent liquid produced by the machine and chug it in one go.")
        self._gameState.tookAction(Actions.YellowPotion)

    def blueButton(self):
        Monitor.print("You press the blue button and the machine whirrs to life.")
        Monitor.print("WHOOSH WHOOSH WHS WHS WHS WSWSWSWSWS (BLUB BLUB BLUB BLUB)",speed=Monitor.SLOW )
        Monitor.print("You grab the bottle of water-like liquid produced by the machine and chug it in one go.",delay)
        self._gameState.tookAction(Actions.BluePotion)
        
    def exitRoom(self):
        self.changeRoom(Rooms.VILLAGEINSIDE)
    
class RoomArarielDialogue(RoomDialog):
    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.ARARIELJEWEL
    availableActions = []
    
    def _onEnter(self):
        ararielDialogLang = {True:"This must be the tear of Arariel.",
                          False:"A jewel sits on top of it."}
        self.description = [f"You find a pedestal surrounded by torches. {ararielDialogLang[self._gameState.fulfillsRequirement(Knowledge.LearnedOfTearOfArariel)]}.",
                            "You approach a majestic pedestal that seems to glow. Though it might be the surrounding torches too."]

        menuOptions={
            'Pick up the jewel':lambda:self.pickupJewel(),
            'Leave': self.exitRoom
        }            
        self.dialog = [(self.description,menuOptions)]
        Monitor.clear()

    def pickupJewel(self):
        Monitor.print("You pick up the beautiful jewel and are surprised by its weight. As you stuff it in your pocket, you hear a faint rumble.")
        Monitor.print("The rumbling grows lowder")
        Monitor.print("You begin to feel light headed. Uh-oh; you now understand the situation: streams of vapor are rising from cracks in the floor.")
        Monitor.print("POISON GAS!!!", speed=Monitor.SLOW)
        self._gameState.updateKnowledge(Knowledge.CollectedTearOfArariel)
        self.exitRoom()
        
    def exitRoom(self):
        self.changeRoom(Rooms.CAVE1)

class RoomEagleDialogue(RoomDialog):
    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.EAGLEDIALOG
    availableActions = []
    
    def _onEnter(self):
        whyHere = (["The lighthouse of Emradir has fallen into disrepair and its fire long since burned out, as the townsfolk are scared to leave the safety of their walls.",
         "The repairs may be beyond your skill, but what you could do is gather magic wood to relight the lighthouse beacon. Will you do this?"],
            {
            'Sure... I guess':lambda:self.acceptQuest(),
            'No way!':lambda:self.declineQuest()
            })
        
        questionsDesc=["You have a lot of questions. Might as well ask the bird, right?"]
        questions={
            'What is this place?':lambda:self.whatPlace(),
            'Why did you summon me here?':lambda:self._advanceDialog(whyHere),
            'How can you talk in my head?':lambda:self.howInMyHead(),
            'Leave the Eagle': self.exitRoom
        }

        self.description = ["The Eagle seems to be telepathically communicating with you.",
                            "It says it does not want to harm you, but can you trust it?"]
        menuOptions={
            'Talk to the Eagle':lambda:self._advanceDialog((questionsDesc,questions)),
            'Leave the Eagle': self.exitRoom
        }            
        self.dialog = [(self.description,menuOptions)]
        Monitor.clear()

    def whatPlace(self):
        Monitor.print("You have ended up on the island of Atlantis. \nThis is the lighthouse of Emradir, which has shed its protective light on the island for hundreds of years.")
        Monitor.print("ATLANTIS??!?", speed=Monitor.SLOW, printline=False)
        Monitor.print("You shout in dismay.")
        Monitor.print("Yes, replied the eagle. The island is cursed; it sinks, only to be brought back by The Beast.")
        Monitor.print("The Beast. At least the Atlanteans aren't good at naming things...")
        Monitor.print("Your arrogance may yet be the end of you. No one who has went to face The Beast has ever returned.")
        self._gameState.updateKnowledge(Knowledge.KnowsOfBeast)

    def acceptQuest(self):
        Monitor.print("Here, take this axe and head to the forest of Vestunm beyond the mountain.")
        self._gameState.tookAction(Actions.EagleQuest)
        self._advanceDialog(None)

    def declineQuest(self):
        Monitor.print("Your destiny is your own.")
        self._advanceDialog(None)

    def howInMyHead(self):
        Monitor.print("The world is a mysterious place, young human.")
        
    def exitRoom(self):
        self.changeRoom(Rooms.LIGHTHOUSE)

class RoomShopkeeperDialogue(RoomDialog):
    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.SHOPKEEPERDIALOG
    availableActions = []
    underAttack = False

    def _getTownAttackListener(self):
        return lambda isAttacked: self.theBeastAttacks() if isAttacked else self.theBeastLeaves()
    
    def _onEnter(self):
        menuOptions={}        
        if self.underAttack:
            self.description = ['You are alone in the shop. You hear sounds of battle outside.']
            if self._gameState.hasAction(Actions.TradedTearToShopkeeper) and \
            not self._gameState.hasAction(Actions.StoleTearFromShopkeeper):
                menuOptions['Steal back the Jewel'] = lambda:self.stealItem(Items.Tear)
            if self._gameState.hasAction(Actions.TradedAxeToShopkeeper) and \
            not self._gameState.hasAction(Actions.StoleAxeFromShopkeeper):
                menuOptions['Steal back the axe'] = lambda:self.stealItem(Items.Axe) 
            if not self._gameState.hasAnyItem([Items.Sword, Items.SwordOfArariel]) and \
            not self._gameState.hasAction(Actions.StoleSwordFromShopkeeper):
                menuOptions['Steal the sword'] = lambda:self.stealItem(Items.Sword, hadBefore=False)
            if not self._gameState.hasItem(Items.Hose) and \
                    self._gameState.fulfillsRequirements([
                    Knowledge.ExaminedPlane,
                    Knowledge.FoundFuelHose]):
                menuOptions['Steal the fuel hose'] = lambda:self.stealItem(Items.Hose)
        else:
            self.description = ['"Welcome stranger. I accept trades and gold." the shopkeeper greets you as you enter.',
                            "You see all kinds of utilities for everyday life; none of which are of interest to you.",
                            "The shopkeeper keeps a close eye on you as you browse the wares."]            
            if not self._gameState.hasAnyItem([Items.Sword, Items.SwordOfArariel]):
                self.description.append("You see a rusty sword hanging on the wall.")
                menuOptions['Examine the sword hanging on the wall'] = self.examineSword
            if self._gameState.fulfillsRequirement(Knowledge.ExaminedPlane) and not self._gameState.hasItem(Items.Hose):
                menuOptions['Inquire about a fuel hose'] = self.askHose            
                    
        menuOptions['Leave the shop'] = self.exitRoom
        
        self.dialog = [(self.description,menuOptions)]
        Monitor.clear()

    def askHose(self):
        Monitor.print("The shopkeeper thinks a while about your request.")
        Monitor.print("After some time he moves to rummage around a pile of goods and digs up a length of a plastic tube.")
        Monitor.print('"Will this do?" He asks. "I could part with it for a few gold coins."')
        Monitor.print("You don't have any money, so you just thank him for his time.")
        self._gameState.updateKnowledge(Knowledge.FoundFuelHose)
        
    
    def examineSword(self):
        Monitor.print("The sword is a bit rusty and very dirty.")
        Monitor.print("You notice a curious indentation in the crossguard; as if something was pried out of it.")
        Monitor.print("The shopkeeper notices your interest and lets you know it is for sale.")

        if self._gameState.hasAnyItem([Items.Tear, Items.Axe]):
            desc = ['You consider if you have anything valuable enough to barter for it.']
            dialog = {}
            if self._gameState.hasItem(Item.Tear):
                dialog["Offer your jewel in trade."] = lambda:self.tradeForSword(Item.Tear)
            if self._gameState.hasItem(Item.Axe):
                dialog["Offer your jewel in trade."] = lambda:self.tradeForSword(Item.Axe)
            dialog["Leave the sword"] = self.refreshScreen
            self._advanceDialog((desc,dialog))

    def stealItem(self,item,hadBefore = True):
        Monitor.print("Now with all the commotion outside, you decide to act.")
        if hadBefore:
            Monitor.print("You steal back your item from the shopkeeper.")
        self._gameState.addItem(item)

        act = self._gameState.tookAction
        {Items.Sword:lambda:act(Actions.StoleSwordFromShopkeeper),
         Items.Axe:lambda:act(Actions.StoleAxeFromShopkeeper),
         Items.Tear:lambda:act(Actions.StoleTearFromShopkeeper)}[item]()
        self.reEnterRoom()

    def theBeastAttacks(self):        
        self.underAttack = True        
        self._gameState.updateKnowledge(Knowledge.SeenBeast)
        if self.roomActive:
            Monitor.print("You hear a screech outside followed by an explosion")
            Monitor.print("The shopkeeper grabs a nearby crowssbow and bolts, then runs outside.                         ")
            self.reEnterRoom()

    def theBeastLeaves(self):
        self.underAttack = False
        if self.roomActive:
            Monitor.print("You hear the sounds of battle die down outside.")
            Monitor.print("The shopkeeper returns behind the counter sweaty and bloodied.")
            self.reEnterRoom()
            

    def exitRoom(self):
        self.changeRoom(Rooms.VILLAGEINSIDE)
