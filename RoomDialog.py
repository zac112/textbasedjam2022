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
    description = ["You enter a huge castle in this small village. You see a royal figure sitting on a throne."]
    descriptionIndex = 0
    connectionDescription = []
    dialog = []
    room = Rooms.LABORATORYINSIDE
    availableActions = []
    underAttack = False
    
    def _getTownAttackListener(self):
        return lambda isAttacked: self.theBeastAttacks() if isAttacked else self.theBeastLeaves()
    
    def _onEnter(self):        
                    
        self.dialog.append(self.getDialog())
        Monitor.clear()

    def getDialog(self):
        description = ["You enter a huge castle in this small village. You see a royal figure sitting on a throne."]        
        kingDialog = (['The king talks with a booming voice: "Who are you?'],
                      {"Answer":self.answerKing})
        
        menuOptions={
            'Talk to King':lambda:self._advanceDialog(kingDialog),
            'Exit': self.exitRoom
        }
        return (description,menuOptions)
    
    def answerKing(self):
        self.getDialog=self.questGiveDialog
        Monitor.print("You explain you crashed your plane and are looking for help.")
        self.reEnterRoom()

    def questGiveDialog(self):
        self._gameState.updateKnowledge(Knowledge.LearnedVillageHistory)
        self.description = ["So you are a stranger. Welcome to the town of Thursten.",
                            "However, know this island is cursed and you only have mere days before it sinks.",
                            "We have a magical device that creates a shield around this town to protect us while submerged,",
                            "however the power source has been stolen by minions of the beast.",
                            "",
                            "If you are able to return it to us, we will allow you to stay under our shield."]        
        acceptDialog = (['Good. We can not spare anyone to aid you. What I can offer you is information:',
                       "We seek a jewel; The tear of Arariel. The beast hid it deep in the caverns of Mount Grear.",
                       "The darkness there is oppressive. Take this light bead, while not much, it should help you navigate the caverns."],
                      {"Thank the king and leave":self.getStone})
        declineDialog = (['Most unfortunate, but you are free to choose your path.',
                          "This offer stands, until the island submerges."],
                      {"Leave":self.exitRoom})
        
        menuOptions={
            'Accept quest': lambda:self.acceptQuest(acceptDialog),
            'Decline quest': lambda:self._advanceDialog(declineDialog)
        }
        return (self.description,menuOptions)

    def returnDialog(self):
        self.description = ["So you have returned. Did you find the Tear of Arariel?",
                            "Our lives depend on it."]
        
        menuOptions={}
        if self._gameState.hasItem(Items.Tear):
            menuOptions["Give jewel"] = lambda: self.giveJewel()
        menuOptions["Apologize and leave"] = self.exitRoom
        
        return (self.description,menuOptions)

    def busyDialog(self):
        self.description = ["The people in the castle are busy and no one has time for you."]
        
        menuOptions={}
        if self._gameState.fulfillsRequirement(Knowledge.FixedLighthouse):
            menuOptions["Go talk to the king"] = self.finishGame
        menuOptions["Leave"] = self.exitRoom
        
        return (self.description,menuOptions)
    
    def giveJewel(self):
        self._gameState.updateKnowledge(Knowledge.ReturnedTearOfArariel)
        Monitor.print("You give the jewel to the king.")
        Monitor.print("He examines it, smiles and hands it off to a nearby person, who quickly leaves the room.")
        
        self._gameState.updateKnowledge(Knowledge.VillagersAcceptYou)
        if self._gameState.fulfillsRequirement(Knowledge.FixedLighthouse):
            self.finishGame()            
        else:
            Monitor.print("The man who was given the jewel returns and whispers to the king.")
            Monitor.print('The king addresses you again:"It seems we still need your help."')
            Monitor.print("The lighthouse that powers our magic has run out of fuel.")
            Monitor.print("The lighthouse keeper kept the lighthouse working, unfortunately he was eaten by the Beast several years ago.")
            Monitor.print("Seek out the means to relight the fire in the lighthouse. Hurry, there is not much time!")
            self.getDialog = self.busyDialog

    def finishGame(self):
        Monitor.print("We thank you. We will begin preparations for submersion immediately.")
        Monitor.print("You are a friend to Thursten and are welcome to stay with us until you decide to leave.")            
        self._gameState.endGame()
            
    def acceptQuest(self, dialog):
        self.getDialog = self.returnDialog
        self._advanceDialog(acceptDialog)
        
    def getStone(self):
        self._gameState.addItem(Items.Lightbead)
        self.exitRoom()
        
    def talkToKing(self, nextDialog):
        self._advanceDialog(nextDialog)
        
    def exitRoom(self):
        self.changeRoom(Rooms.VILLAGEINSIDE)

    def theBeastAttacks(self):
        self.underAttack = True
        if self.roomActive:
            Monitor.print("Everyone is alerted by explosions on the outside. They rush out and drag you along.")
            self.exitRoom()

    def theBeastLeaves(self):
        self.underAttack = False
        
class RoomLaboratoryInside(RoomDialog):
    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.LABORATORYINSIDE
    availableActions = []
    
    def _onEnter(self):            
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
    browseOptions = ['Browse through the wares',
                  "Keep browsing the wares. There must be something of use.",
                  "Keep browsing. You begin to lose faith of finding anything useful here.",
                  "Dig through a pile of useless-looking junk."]
    browseIndex = 0
    
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
                menuOptions['Steal the fuel hose'] = lambda:self.stealItem(Items.Hose, hadBefore=False)
        else:
            if self._gameState.fulfillsRequirement(Knowledge.LearnedLanguage):
                firstLine ='"Welcome stranger. I accept trades and gold." the shopkeeper greets you as you enter.'
            else:
                firstLine ='The shopkeeper greets you as you enter in a language you do not undestand.'
            self.description = [firstLine,
                            "You see all kinds of utilities for everyday life; none of which are of interest to you.",
                            "The shopkeeper keeps a close eye on you as you browse the wares."]            
            if not self._gameState.hasAnyItem([Items.Sword, Items.SwordOfArariel]):
                self.description.append("You see a rusty sword hanging on the wall.")
                menuOptions['Examine the sword hanging on the wall'] = self.examineSword
            if self._gameState.fulfillsRequirements([Knowledge.ExaminedPlane, Knowledge.LearnedLanguage]) and \
            not self._gameState.hasItem(Items.Hose):
                menuOptions['Inquire about a fuel hose'] = self.askHose            
        if not self._gameState.hasItem(Items.Hose):
            try: menuOptions[self.browseOptions[self.browseIndex]] = self.browse
            except: pass
        menuOptions['Leave the shop'] = self.exitRoom
        
        self.dialog = [(self.description,menuOptions)]
        Monitor.clear()

    def browse(self):
        self.browseIndex += 1
        Monitor.print("You go through some stuff, but it's all junk.")
        if self.browseIndex >= len(self.browseOptions):
            self._gameState.updateKnowledge(Knowledge.FoundFuelHose)
            Monitor.print("You rummage around a pile of goods and see a piece of a plastic tube.")
            Monitor.print("Too bad you don't have anything to buy it with...                    ")
        self.reEnterRoom()
            
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
                dialog["Offer your axe in trade."] = lambda:self.tradeForSword(Item.Axe)
            dialog["Leave the sword"] = self.refreshScreen
            self._advanceDialog((desc,dialog))

    def tradeForSword(self, item):
        Monitor.print("The shopkeeper examines your offer and accepts the trade.")
        self._gameState.removeItem(item)
        self._gameState.addItem(Items.Sword)

        act = self._gameState.tookAction
        {Items.Axe:lambda:act(Actions.TradedAxeToShopkeeper),
         Items.Tear:lambda:act(Actions.TradedTearToShopkeeper)}[item]()
        
        
    def stealItem(self,item,hadBefore = True):
        Monitor.print("Now with all the commotion outside, you decide to act.")
        if hadBefore:
            Monitor.print("You steal back your item from the shopkeeper.")
        self._gameState.addItem(item)

        act = self._gameState.tookAction
        {Items.Sword:lambda:act(Actions.StoleSwordFromShopkeeper),
         Items.Axe:lambda:act(Actions.StoleAxeFromShopkeeper),
         Items.Tear:lambda:act(Actions.StoleTearFromShopkeeper),
         Items.Hose:lambda:act(Actions.StoleHoseFromShopkeeper)}[item]()
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
