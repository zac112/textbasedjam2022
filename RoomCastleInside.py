from Knowledge import Knowledge
from Rooms import Rooms
from Monitor import Monitor
from MenuItem import MenuItem
from GameTime import GameTime
from Room import *

class RoomCastleInside(Room):

    descriptionIndex = 0
    connectionDescription = []
    room = Rooms.CASTLEINSIDE
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
        self.advanceDialog(nextDialog)
        
    def talkToKing(self, nextDialog):
        self.advanceDialog(nextDialog)
        
    def advanceDialog(self, nextDialog):
        if nextDialog: self.dialog.append(nextDialog)
        else: self.dialog.pop()
        
    def exitRoom(self):
        self.changeRoom(Rooms.VILLAGEINSIDE)
        
    def _getMenuItems(self) -> list:
        return list(self.dialog[-1][1].keys())

    def _getMenuString(self, item):
        return item
    
    def _menuAccept(self):                
        self.dialog[-1][1][self._getMenuItems()[self.menuindex]]()
        self.description,dialog = self.dialog[-1]
        self.refreshScreen()
