from Enums import *
from Monitor import Monitor
from MenuItem import MenuItem
from Room import *

from threading import Thread
from time import sleep

import random

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

    def reEnterRoom(self):
        pass
    
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
    class Torch(Thread):
            def __init__(self, pos, lock, room):
                Thread.__init__(self)
                self.anims = ["ý","ỹ","ỳ"]
                self.pos = pos
                self.lock = lock
                self.running = True
                self.room = room

            def run(self):                
                while self.running:
                    sleep(random.random())
                    if not self.running: break                    
                    if self.pos in self.room.visibleCells:
                        self.lock.acquire()
                        Monitor.draw(self.anims[random.randint(0,2)],pos=self.pos)
                        self.lock.release()

            def terminate(self):
                self.running = False
                
    descriptionIndex = 0
    description = ["You stand in the middle of a large marketplace."]
    connectionDescription = ["Enter the cave?"]
    room = Rooms.CAVEINSIDE
    availableActions = []
    pos = (2,15)
    textmap = """                                         ¤
             ...»                        ¤
             .                           ¤
            ..                           ¤
            y.                           ¤
           ....                          ¤
           ....                          ¤
           ....                          ¤
            ....  y......y.......        ¤
             ...................y        ¤
             y....................       ¤
             ...     ....     ....       ¤
           .....     ....     ....       ¤
▓▓▒░...........      ....     y...       ¤
▓▓▒░..........y       ..      ....       ¤
▓▓▒..y.........       ..      .......░▒▓▓¤
                      ..       ......░▒▓▓¤
                      ..       ...y..░▒▓▓¤
                  «.....                 ¤
                                         ¤""".split('¤')

    torchlight = """...░.¤
.▒▓▒.¤
░▓y▓░¤
.▒▓▒.¤
..░..¤""".split("¤")
        
    def _onEnter(self):
        Monitor.clear()

        self.visibleCells = self.floodFill(self.pos)
        self.forbidden = []
        self.torches = []
        for y,line in enumerate(self.textmap,1):
            self.textmap[y-1] = list(line)
            for x,c in enumerate(line):
                if c in self._getForbiddenChars():
                    self.forbidden.append((x,y))
                if c in ['y']:
                    self.torches.append(self.Torch((x,y),self._gameState.lock, self))
        self.lightTorches()
        
        self.doors = self._getDoors()

    def _getDoors(self):
        return {
            (1,14):lambda:self.changeRoom(Rooms.CAVEENTRANCE),
            (1,15):lambda:self.changeRoom(Rooms.CAVEENTRANCE),
            (1,16):lambda:self.changeRoom(Rooms.CAVEENTRANCE),
            (17,2):lambda:self.changeRoom(Rooms.CAVE1),
            (19,19):lambda:self.changeRoom(Rooms.CAVE2),
            (41,16):lambda:self.changeRoom(Rooms.CAVEEXIT),
            (41,17):lambda:self.changeRoom(Rooms.CAVEEXIT),
            (41,18):lambda:self.changeRoom(Rooms.CAVEEXIT)
            }

    def _onExit(self):
        for t in self.torches:
            t.terminate()

    def _getForbiddenChars(self):
        return [' ']
    
    def lightTorches(self):
        for pos in [t.pos for t in self.torches]:
            for y, line in enumerate(self.torchlight,-3):                
                for x, char in enumerate(line,-3):
                    mapx,mapy = x+pos[0],y+pos[1]           
                    try:
                        if self.textmap[mapy][mapx] != '.' or char == "\n" or mapy < 0 or mapx < 0: continue                        
                        self.textmap[mapy][mapx] = char
                    except: pass

        for t in self.torches:
            t.start()
        
    def refreshScreen(self):
        if not self.roomActive :return
                
        Monitor.clear()
        for y,line in enumerate(self.textmap):
            for x,c in enumerate(line):
                if (x,y) not in self.visibleCells: continue
                Monitor.draw(self.textmap[y][x].replace("."," "),pos=(x,y+1))

        self.drawPlayer()

    def move(self, movement):
        if not self.roomActive :return
        x,y = self.pos
        newPos = movement(x,y)
        if newPos in self.forbidden: return

        self.visibleCells = self.floodFill(newPos)        
        self.pos = newPos
        self.refreshScreen()
        self.doors.get(self.pos,lambda:None)()

    #returns set of visible cells from pos
    def floodFill(self, pos) -> set:
        def hasSightline(player,target,textmap):
            sign = lambda a: 0 if a==0 else a//abs(a)            
            x,y = target
            while (x,y) != player:                                
                x -= sign(x-player[0])
                if textmap[y][x] in self._getForbiddenChars():return False
                y -= sign(y-player[1])
                if textmap[y][x] in self._getForbiddenChars():return False
            return True
            
        pos = (pos[0],pos[1]-1)
        queue = [pos]
        visited = set()
        while queue:            
            x,y = queue.pop(0)
            try: self.textmap[y][x]
            except: continue
                        
            if (x,y) in visited: continue
            if not hasSightline(pos,(x,y),self.textmap):continue
            visited.add((x,y))
            if self.textmap[y][x] in self._getForbiddenChars(): continue
            
            queue.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])            
        return visited
            
    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]


class RoomCave1Inside(RoomCaveInside):
    room = Rooms.CAVE1
    availableActions = []
    pos = (14,2)
    textmap = """
                                        ¤
   .....    »..............y........    ¤
   .....       y....#####  .       .    ¤
   .........    ..###      .  ........  ¤
   .....   .    .##        .  . .    .  ¤
           .    .  ............ . .. .  ¤
           .    .  .   .        #  ...  ¤
  ..............y  .   .    .           ¤
  .        #    .  .   ...............  ¤
  ............  .      #        ......  ¤
             .  ..#........#    ......  ¤
      #.......  .   .     .     ......  ¤
         .      .   .     .     ......  ¤
         .          .  .......  ##.###  ¤
         .          .  .......   #.#    ¤
       ..............  .......   #.##   ¤
       .               .......   #..#   ¤
   .........           .......   ####   ¤
   .........           ..┌¥┐..          ¤
   .........           ..└-┘..          ¤
   .........           .......          ¤ """.split('¤')
    
    def _getDoors(self):
        return { (13,2):lambda:self.changeRoom(Rooms.CAVEINSIDE) }
    
    def _getForbiddenChars(self):
        return [' ','└','-','┘','┌','┐','#']
