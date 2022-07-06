from Enums import *
from Monitor import Monitor
from MenuItem import MenuItem
from Room import *

class RoomInside(Room):
    def _registerMenu(self):
        self._gameState.registerInput(self.up, "up")
        self._gameState.registerInput(self.down, "down")
        self._gameState.registerInput(self.left, "left")
        self._gameState.registerInput(self.right, "right")

    def _unregisterMenu(self):
        self._gameState.unregisterInput(self.up, "up")
        self._gameState.unregisterInput(self.down, "down")
        self._gameState.unregisterInput(self.left, "left")
        self._gameState.unregisterInput(self.right, "right")

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
        self.doors.get(self.pos,lambda:None)()
            
        
    def right(self):
        self.move(lambda x,y: (min(x+1,len(self.textmap[0])), y))        
        
    def left(self):
        self.move(lambda x,y: (max(x-1,1), y))
        
    def down(self):
        self.move(lambda x,y: (x, min(y+1,len(self.textmap[0]))))
        
    def up(self):
        self.move(lambda x,y: (x, max(y-1,1)))

class RoomVillageInside(RoomInside):
            
    descriptionIndex = 0
    description = ["You stand in the middle of a large marketplace."]
    connectionDescription = []
    room = Rooms.VILLAGEINSIDE
    availableActions = []
    pos = (14,14)
    textmap = """╔═══════════════════════════╗¤
║      ,,,,,,,,,,,,         ║¤
║     /░░░░░░░░░░░░\        ║¤
║    /│            │\       ║¤
║     │     ___    │        ║¤
║     │_____███____│        ║¤
║          .▒▒▒.            ║¤
║          .▒▒▒.            ║¤
║   /¯¯¯\  .▒▒▒. /¯¯¯\      ║¤
║   │ _ │  .▒▒▒. │ _ │      ║¤
║   │_█_│...▒▒▒..│_█_│      ║¤
║     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒        ║¤
║           ▒▒▒             ║¤
║           ▒▒▒             ║¤
╚═══════════■■■═════════════╝¤""".split('¤')
    
    def _onEnter(self):
        Monitor.clear()
        
        self.forbidden = []
        for y,line in enumerate(self.textmap,1):
            for x,c in enumerate(line):
                if c in [',','╚','═','/','_','╝','║','│','\\']:
                    self.forbidden.append((x,y))
        self.doors = {
            (13,6):lambda:self.changeRoom(Rooms.CASTLEINSIDE),
            (14,6):lambda:self.changeRoom(Rooms.CASTLEINSIDE),
            (15,6):lambda:self.changeRoom(Rooms.CASTLEINSIDE),
            (20,11):lambda:self.changeRoom(Rooms.LABORATORYINSIDE),
            #(7,11):,
            (13,15):lambda:self.changeRoom(Rooms.VILLAGE),
            (14,15):lambda:self.changeRoom(Rooms.VILLAGE),
            (15,15):lambda:self.changeRoom(Rooms.VILLAGE)
            }

class RoomCaveInside(RoomInside):
            
    descriptionIndex = 0
    description = ["You stand in the middle of a large marketplace."]
    connectionDescription = ["Enter the cave?"]
    room = Rooms.CAVEINSIDE
    availableActions = []
    pos = (2,15)
    textmap = """                                        ¤
             ...»                       ¤
             .                          ¤
            ..                          ¤
            y.                          ¤
           ....                         ¤
           ....                         ¤
           ....                         ¤
            ....  y......y.......       ¤
             ....................       ¤
             y....................      ¤
             ...     ....     ....      ¤
           .....     ....     ....      ¤
.▓▒░...........      ....     y...      ¤
.▓▒░..........y       ..      ....      ¤
.▓▒..y.........       ..      .......░▒▓¤
                      ..       ......░▒▓¤
                      ..       ...y..░▒▓¤
                  «.....                ¤
                                        ¤""".split('¤')

    torchlight = """.░░░░.¤
░▒▓▒░¤
░▓y▓░¤
░▒▓▒░¤
.░░░.¤""".split("¤")
    
    torches = ["ý","ỹ","ỳ"]
    def _onEnter(self):
        Monitor.clear()
        
        self.forbidden = []
        self.torches = []
        for y,line in enumerate(self.textmap,1):
            for x,c in enumerate(line):
                if c in [' ','╚','═','/','_','╝','║','│','\\']:
                    self.forbidden.append((x,y))
                if c in ['y']:
                    self.torches.append((x,y))
        self.lightTorches()
        
        self.doors = {
            (1,14):lambda:self.changeRoom(Rooms.CAVEENTRANCE),
            (1,15):lambda:self.changeRoom(Rooms.CAVEENTRANCE),
            (1,16):lambda:self.changeRoom(Rooms.CAVEENTRANCE),
            (17,2):lambda:self.changeRoom(Rooms.CAVE1),
            (9,19):lambda:self.changeRoom(Rooms.CAVE2),
            (39,16):lambda:self.changeRoom(Rooms.CAVEEXIT),
            (39,17):lambda:self.changeRoom(Rooms.CAVEEXIT),
            (39,18):lambda:self.changeRoom(Rooms.CAVEEXIT)
            }

    def lightTorches(self):
        for y,line in enumerate(self.textmap):
            self.textmap[y] = list(line)
        
        for pos in self.torches:
            for y, line in enumerate(self.torchlight,-3):
                for x, char in enumerate(line,-3):
                    mapx,mapy = x+pos[0],y+pos[1]           
                    try:
                        if self.textmap[mapy][mapx] != '.' or char == "\n" or mapy < 0 or mapx < 0: continue                        
                        self.textmap[mapy][mapx] = char
                    except: pass
        
        for y,line in enumerate(self.textmap):
            self.textmap[y] = "".join(line)

    def refreshScreen(self):
        if not self.roomActive :return

        Monitor.clear()
        [Monitor.draw(line.replace("."," ")) for line in self.textmap]
        self.drawPlayer()

    def move(self, movement):
        x,y = self.pos
        newPos = movement(x,y)
        if newPos in self.forbidden: return
        Monitor.draw(self.textmap[y-1][x].replace("."," "), pos=self.pos)
        self.pos = newPos
        self.drawPlayer()
        self.doors.get(self.pos,lambda:None)()
        
    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]
