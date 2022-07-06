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
        kingDialog = (["The king talks with a booming voice:  Who are you?"],
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
            Monitor.print("You think about entering the room with the machine. You decide against it.", delay=True)
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
            Monitor.print("Several scientists (presumably) barge in the room and begin questioning you.",delay=True)
            Monitor.print("To your great surprise, you undestand these people and are able to talk your way out of being thrown in jail.",delay=True)
            self._gameState.updateKnowledge(Knowledge.LearnedLanguage)
            self.exitRoom()
        return a
    
    def redButton(self):
        Monitor.print("You press the red button and the machine whirrs to life.",delay=True)
        Monitor.print("WHRR R R GZZGZZ (BLUB BLUB BLUB BLUB)",speed=Monitor.SLOW ,delay=True)
        Monitor.print("You grab the bottle of blood-like liquid produced by the machine and chug it in one go.",delay=True)
        self._gameState.tookAction(Actions.RedPotion)
        
    def yellowButton(self):
        Monitor.print("You press the yellow button and the machine whirrs to life.",delay=True)
        Monitor.print("CHUGCHUG CHCH CGCGCGCG (BLUB BLUB BLUB BLUB)",speed=Monitor.SLOW ,delay=True)
        Monitor.print("You grab the bottle of almost transparent liquid produced by the machine and chug it in one go.",delay=True)
        self._gameState.tookAction(Actions.YellowPotion)

    def blueButton(self):
        Monitor.print("You press the red button and the machine whirrs to life.",delay=True)
        Monitor.print("WHOOSH WHOOSH WHS WHS WHS WSWSWSWSWS (BLUB BLUB BLUB BLUB)",speed=Monitor.SLOW ,delay=True)
        Monitor.print("You grab the bottle of water-like liquid produced by the machine and chug it in one go.",delay=True)
        self._gameState.tookAction(Actions.BluePotion)
        
    def exitRoom(self):
        self.changeRoom(Rooms.VILLAGEINSIDE)
    
