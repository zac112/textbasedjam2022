from Knowledge import Knowledge
from Rooms import Rooms
from Monitor import Monitor
from MenuItem import MenuItem
from GameTime import GameTime
from Room import *

class RoomVillageInside(Room):
#region events
    class VillageInside(MenuItem):
        def getMenuString(self, room : Rooms):            
            return "Head inside the town."

        def selectFromMenu(self, fromRoom : Rooms):
            Monitor.print("You decide to ignore them and keep walking towards the gates. ", delay=1)
            Monitor.print("The soldiers do not hesitate to impale you with their spear. You died.", delay=1)
            

        def getAllowedTimes(self) -> list:
            return [GameTime.DUSK,
                    GameTime.NOON,
                    GameTime.DAWN]
#endregion events
            
    descriptionIndex = 0
    description = ["You stand in the middle of a large marketplace."]
    connectionDescription = []
    room = Rooms.VILLAGEINSIDE
    availableActions = []
    textmap = """╔═══════════════════════════╗¤
║      ,,,,,,,,,,,,         ║¤
║     /░░░░░░░░░░░░\        ║¤
║    /│            │\       ║¤
║     │            │        ║¤
║     │_____███____│        ║¤
║          .▒▒▒.            ║¤
║    ___   .▒▒▒.  ___       ║¤
║   /   \  .▒▒▒. /   \      ║¤
║   │   │  .▒▒▒. │   │      ║¤
║   │_█_│...▒▒▒..│_█_│      ║¤
║     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒        ║¤
║           ▒▒▒             ║¤
║           ▒▒▒             ║¤
╚═══════════▒▒▒═════════════╝¤""".split('¤')
    
    def _onEnter(self):
        Monitor.clear()
        self.pos = (15,14)
        
        self.forbidden = []
        for y,line in enumerate(self.textmap,1):
            for x,c in enumerate(line):
                if c in [',','╚','═','/','_','╝','║','│','\\']:
                    self.forbidden.append((x,y))            

    def enterRoom(self):
        self.roomActive = True
        self._registerEvents()
        self._registerInput(self._gameState)
        self._onEnter()
        self.refreshScreen()
        
    def _registerInput(self, gameState : GameState):
        gameState.registerInput(self.up, "up")
        gameState.registerInput(self.down, "down")
        gameState.registerInput(self.left, "left")
        gameState.registerInput(self.right, "right")

    def _unregisterInput(self, gameState : GameState):
        gameState.unregisterInput(self.up, "up")
        gameState.unregisterInput(self.down, "down")
        gameState.unregisterInput(self.left, "left")
        gameState.unregisterInput(self.right, "right")

    def refreshScreen(self):
        if not self.roomActive :return

        Monitor.clear()
        [Monitor.draw(line) for line in self.textmap]
        self.drawPlayer()
        
    def drawPlayer(self):
        Monitor.draw('☺',pos=self.pos)

    def move(self, movement):
        x,y = self.pos
        newPos = movement(x,y)
        if newPos in self.forbidden: return
        Monitor.draw(self.textmap[y-1][x], pos=self.pos)
        self.pos = newPos
        self.drawPlayer()
        
    def right(self):
        self.move(lambda x,y: (min(x+1,len(self.textmap[0])), y))        
        
    def left(self):
        self.move(lambda x,y: (max(x-1,1), y))
        
    def down(self):
        self.move(lambda x,y: (x, min(y+1,len(self.textmap[0]))))
        
    def up(self):
        self.move(lambda x,y: (x, max(y-1,1)))
        
