from Knowledge import Knowledge
from Rooms import Rooms
from Monitor import Monitor
from MenuItem import MenuItem
from GameTime import GameTime
from Room import *

class RoomCastleInside(Room):

    descriptionIndex = 0
    description = ["You stand in the middle of a large marketplace."]
    connectionDescription = []
    room = Rooms.CASTLEINSIDE
    availableActions = []
    
    def _onEnter(self):
        self.dialog = []
        menuOptions={
            'Talk to King':lambda:print("You talked."),
            'Exit': self.exitRoom
        }            
        self.dialog.append(menuOptions)                    
        Monitor.clear()

    def _displayMenuItems(self):
        Monitor.setCursorPos(self.menupos)
        for i, item in enumerate(self._getMenuItems()):
            if i==self.menuindex: item = '>'+item+'<'
            else: item = " "+item+" "
            Monitor.print(item, speed=Monitor.FAST)
        
    def exitRoom(self):
        self.changeRoom(Rooms.VILLAGEINSIDE)
        
    def _getMenuItems(self) -> list:
        return list(self.dialog[-1].keys())

    def _menuAccept(self):
        self.dialog[-1][self._getMenuItems()[self.menuindex]]()
