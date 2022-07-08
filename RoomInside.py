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

    def _shouldDisplayApproximateTime(self):
        return False
    
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
    underAttack = False
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

    def _getTownAttackListener(self):
        return lambda isAttacked: self.theBeastAttacks() if isAttacked else self.theBeastLeaves()
    
    def _onEnter(self):
        Monitor.clear()
        
        self.forbidden = []
        for y,line in enumerate(self.textmap,1):
            for x,c in enumerate(line):
                if c in self._getForbiddenChars():
                    self.forbidden.append((x,y))
        self.doors = self._getDoors()

    def _getDoors(self):
        return {
            (13,6):self.enterCastle,
            (14,6):self.enterCastle,
            (15,6):self.enterCastle,
            (20,11):self.enterLab,
            (7,11):lambda:self.changeRoom(Rooms.SHOPKEEPERDIALOG),
            (13,15):lambda:self.changeRoom(Rooms.VILLAGE),
            (14,15):lambda:self.changeRoom(Rooms.VILLAGE),
            (15,15):lambda:self.changeRoom(Rooms.VILLAGE)
            }
    
    def _getForbiddenChars(self):
        return [',','╚','═','/','_','╝','║','│','\\']
    
    def theBeastAttacks(self):        
        self.underAttack = True
        if self.roomActive:
            Monitor.print("You hear a screech and look up. You see a monstrous flying creature.")
            Monitor.print("A house near you explodes! The town is under attack!")
            Monitor.print("Townsfolk emerge from their houses to fight the Beast.")

    def theBeastLeaves(self):
        self.underAttack = False
        if self.roomActive:
            Monitor.print("The creature stops attacking the town and retreats towards the mountains")

    def enterCastle(self):
        if self.underAttack:
            Monitor.print("There is nobody here; they're all fighting outside!")
        else:
            self.changeRoom(Rooms.CASTLEINSIDE)

    def enterLab(self):
        if self._gameState.fulfillsRequirement(Knowledge.LearnedLanguage):
            Monitor.print("You think about entering the room with the machine (and angry scientists).")
            Monitor.print("...You decide against it.")
        else:
            self.changeRoom(Rooms.LABORATORYINSIDE)

class RoomCaveInside(RoomInside):
    class Torch(Thread):
            def __init__(self, pos, lock, room):
                Thread.__init__(self)
                self.anims = ["ý","ỹ","ỳ"]
                self.pos = pos
                self.lock = lock
                self.running = True
                self.room = room
                self.torch = 'y'

            def run(self):                
                while self.running:
                    sleep(random.random())
                    self.torch = random.sample(self.anims,1)[0]
                    if not self.running: break
                    if (self.pos[0],self.pos[1]-1) in self.room.visibleCells:
                        self.lock.acquire()                        
                        Monitor.draw(self.torch, pos=self.pos)
                        self.lock.release()

            def terminate(self):
                self.anims=[" "]
                self.running = False
                
    descriptionIndex = 0
    description = ["You stand in the middle of a large marketplace."]
    connectionDescription = ["Enter the cave?"]
    room = Rooms.CAVEINSIDE
    availableActions = []
    visibility = 1000
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
        self.visibility = 1000
        Monitor.clear()
        self.visibleCells = self.floodFill(self.pos, distance=self.visibility)
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
            (40,16):lambda:self.changeRoom(Rooms.CAVEEXIT),
            (40,17):lambda:self.changeRoom(Rooms.CAVEEXIT),
            (40,18):lambda:self.changeRoom(Rooms.CAVEEXIT)
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
                for torch in self.torches:
                    if (x,y) == torch.pos:
                        Monitor.draw(torch.torch,pos=(x,y))
                else:
                    Monitor.draw(self.textmap[y][x].replace("."," "),pos=(x,y+1))

        self.drawPlayer()

    def move(self, movement):
        x,y = self.pos
        newPos = movement(x,y)
        if newPos in self.forbidden: return
        if self.isLethalTile(newPos): self._gameState.endGame()

        self.visibleCells = self.floodFill(newPos, distance=self.visibility)        
        self.pos = newPos
        self.refreshScreen()
        if self._gameState.hasItem(Items.Lightbead):
            self.lightSurroundings()
        self.doors.get(self.pos,lambda:None)()

    def lightSurroundings(self):
        x,y = self.pos
        y -= 1
        for x1,y1 in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if self.textmap[y1][x1] == ".":
                Monitor.draw("░",pos=(x1,y1+1))
        
    #returns set of visible cells from pos
    def floodFill(self, pos, distance=3) -> set:
        def hasSightline(player,target,textmap):
            sign = lambda a: 0 if a==0 else a//abs(a)            
            x,y = target
            while (x,y) != player:                                
                x -= sign(x-player[0])
                if textmap[y][x] in self._getForbiddenChars():return False
                y -= sign(y-player[1])
                if textmap[y][x] in self._getForbiddenChars():return False
            return True

        level = 0
        pos = (level,(pos[0],pos[1]-1))
        queue = [pos]
        visited = set()
        while queue:            
            level,(x,y) = queue.pop(0)

            if level > distance:continue
            try: self.textmap[y][x]
            except: continue
                        
            if (x,y) in visited: continue
            if not hasSightline(pos[1],(x,y),self.textmap):continue
            visited.add((x,y))
            if self.textmap[y][x] in self._getForbiddenChars(): continue
            newLevel = level+1
            queue.extend([(newLevel,(x+1,y)),
                          (newLevel,(x-1,y)),
                          (newLevel,(x,y+1)),
                          (newLevel,(x,y-1))])            
        return visited
            
    def _getConnectionString(self, fromRoom):
        return {Rooms.CAVEENTRANCE: self.connectionDescription[self.descriptionIndex]
                ,Rooms.CAVEEXIT: self.connectionDescription[self.descriptionIndex]
                }[fromRoom]

    def isLethalTile(self, pos):
        return False

class RoomCave1Inside(RoomCaveInside):
    room = Rooms.CAVE1
    availableActions = []    
    pos = (14,2)
    #pos = (27,17)    
    collapsing = False
    textmap = """
                                        ¤
   .....    ».......................    ¤
   .....       y....#####  .       .    ¤
   .........    ..###      .  ........  ¤
   .....   .    .##        .  . .    .  ¤
           .    .  ............ . .. .  ¤
           .    .  .   .        #  ...  ¤
  ...............  .   .    .           ¤
  .        #    .  .   ...............  ¤
  ............  .      #        ......  ¤
             .  ..#........#    ......  ¤
      #.......  .   .     .     ......  ¤
         .      .   .   .....   ......  ¤
         .    .     .  .y...y.  ##.###  ¤
         .    .     .  .......   #.#    ¤
       ..............  .y...y.   #.##   ¤
       .          . .  .......   #..#   ¤
   .........      . .  .y...y.   ####   ¤
   ..................  .......          ¤
   .........           .y...y.          ¤
   .........           .......          ¤
                       .y...y.          ¤
                       .......          ¤
                       .y...y.          ¤
                       ..┌¥┐..          ¤
                       ..└-┘..          ¤
                       .y...y.          ¤
                       .......          ¤
                                        ¤""".split('¤')

    def _onEnter(self):        
        super()._onEnter()
        self.visibility = 5
        if self._gameState.fulfillsRequirement(Knowledge.CollectedTearOfArariel):
            
            self.startCollapse()
            self.collapsing = True

    def startCollapse(self):
        if self.collapsing: return
        self._gameState.registerEvent(self.collapse, self._gameState.getTick()+2)
        self.nextCollapses = [(27,27)]

    def collapse(self, ticks):
        newPositions = []
        for pos in self.nextCollapses:
            x,y = pos
            try:self.textmap[y-1][x]
            except:continue
            
            if self.textmap[y-1][x] in [" ","¤"]:continue
            self.textmap[y-1][x] = "¤"            
            if pos in self.visibleCells: Monitor.draw("¤",pos=pos)
            newPositions.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])

        self.nextCollapses = newPositions        
        if self.nextCollapses:
            self._gameState.registerEvent(self.collapse, ticks+random.randint(1,2))
            
    def _getDoors(self):
        if self.collapsing:
            option = lambda:Monitor.print("You admire the majestic pedestal of the tear of Arariel while the cavern around you is collapsing.",delay=False)
        else:
            option = lambda:self.changeRoom(Rooms.ARARIELJEWEL)
            
        return {(13,2):lambda:self.changeRoom(Rooms.CAVEINSIDE),
                (27,25):option
                }
    
    def _getForbiddenChars(self):
        return [' ','└','-','┘','┌','┐','#']

    def isLethalTile(self, pos):
        result = self.textmap[pos[1]-1][pos[0]]=="¤"
        if result:
            for t in self.torches:
                t.terminate()
        return result

class RoomForestInside(RoomVillageInside):
    room = Rooms.FORESTINSIDE
    availableActions = []    
    pos = (15,27)
    textmap ="""#############≡#########≡≡######≡######¤ 
#####≡≡≡≡###≡≡########≡##≡≡###########¤ 
###≡≡#####≡≡,≡≡≡≡≡≡###################¤ 
#########≡≡≡≡≡≡≡≡≡≡≡≡≡######≡≡###≡≡≡≡≡¤ 
###\'\'\'####≡≡≡≡≡≡≡≡≡≡≡≡ ########≡#≡≡≡#¤ 
##,##,\',\',,≡≡≡≡≡≡≡≡≡\',\'.\'≡≡≡#≡≡≡#####¤ 
≡≡≡\',\'\'...\',≡≡≡≡≡≡≡≡≡\'\'≡≡≡≡,####.##,\'¤ 
≡≡≡≡≡≡≡\'.\'\',≡≡≡≡≡≡≡≡≡≡≡≡≡≡.\',# \'\',,,¤
..≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡\',\'. .,,..,\'¤
,\'.  ,≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡\',, ., ,,.,.,, ¤
.,.\' ,,.,\'≡≡≡≡≡≡≡≡≡≡≡\'\'\'.\'\' . \' .\'  ¤
,,, , ,. \'≡≡≡≡≡≡≡≡≡≡≡\'\'\'.  ,\'. \'.,,,¤
..,\'.\'...,≡≡≡≡≡≡≡≡≡≡≡,,\', , ,\' \'. \',¤
\',\'.\'.,.,,≡≡≡≡≡≡≡≡≡≡≡\'.\',\'..\' \'.. ¡ ¤
\'\'\'....\',,≡≡≡≡≡≡≡≡≡≡≡,...  ,,.\'\'.\', ¤
,., \'. .\'≡≡≡≡≡▀≡≡≡≡≡≡≡\' .,\',\'.\'\',,  ¤
 ,.,..¡ ,,,...░,. .   \' ,., .. .\'. \'¤
.\' ...  \'\'.\'\'.░,\'\' .,¡ .,. ... ..,\'\'¤
.,\'\'¡ ,\'..\' \'░,░. ...¡  ..,,,,\' . ¡ ¤
. ,,. ,¡,, ,.░░░,.,.\', .\'\'.,  \' \' ¡¡ ¤
. . ,..  ,.,,░░░.. ,,, \' ,.\',,  , ¡ ¤
\'.\'  , ..\'.,. ░░\'\'..,.\'..,.,\'\'\'.\',,.¤
\'.,.  \'.,,  ,░░░. ¡ ,.\', .\',.. \' ,  ¤
,\',.,¡  \'\'\'.,░░░...  \', ., ,,,, .\'\',¤
\'\'\'. ,\'\'  \',\'░░░, ,,, ..\'\' , . ..\'. ¤
 ¡ .  ,..,,,,░░░.\' ¡ .,,\',\'\' ¡ , ¡ ,¤
.\' ,, ,,\',.\'\'░░░\'.\',.. ,, .,,,.\'.\' .¤
                                    ¤""".split('¤')

        
    def _getDoors(self):
        width = len(self.textmap[0])
        height = len(self.textmap)-1
        doors = {(15,16):self.chopWood}
        bottom = {(x,height):lambda:self.changeRoom(Rooms.FOREST) for x in range(width)}
        left = {(1,y):lambda:self.changeRoom(Rooms.FOREST) for y in range(height)}
        right = {(width-2,y):lambda:self.changeRoom(Rooms.FOREST) for y in range(height)}
        doors.update(bottom)
        doors.update(left)
        doors.update(right)
        
        return doors

    def _getForbiddenChars(self):
        return ['#','≡']
    
    def chopWood(self):
        if self._gameState.hasItem(Items.Axe):
            Monitor.print("You chop some magical wood")
            self._gameState.addItem(Items.Wood)
        else:
            Monitor.print("You could chop wood here, but you lack the tools")
