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
        if nextDialog: self.dialog.append(nextDialog)
        else: self.dialog.pop()
        
class RoomCastleInside(RoomDialog):

    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.LABORATORYINSIDE
    availableActions = []
    
    def _onEnter(self):
        self.description = ["You enter a huge castle in this small village. You see a royal figure sitting on a throne."]
        self.dialog = []
        kingDialogLang = {True:": Who are you?",
                          False:", but you do not understand him."}
        kingDialog = (["The king talks with a booming voice"+kingDialogLang[self_gameState.fulfillsRequirement(Knowledge.LearnedLanguage)]],
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
        Monitor.print("You begin to feel light headed. Uh-oh; you now understand the situation:")
        Monitor.print("POISON GAS!!!", speed=Monitor.SLOW)
        self._gameState.updateKnowledge(Knowledge.CollectedTearOfArariel)
        self.exitRoom()
        
    def exitRoom(self):
        self.changeRoom(Rooms.CAVE1)
