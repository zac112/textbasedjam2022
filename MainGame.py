from Room import *
from Enums import *
from RoomDialog import *
from RoomInside import *

from Clock import Timer
from InputHandler import InputHandler
from GameState import GameState
from Monitor import Monitor
from threading import Lock


import sys
import time

lock = Lock()
timer = Timer(0,"Clock", lock)
inp = InputHandler(1,"Input", lock)

def quitGame():
    timer.stopCounting()
    inp.stopListening()
    input("Game over.")
    sys.exit(0)
    
def initGame():
    timer.startCounting()    
    inp.startListening()
    inp.registerObserver(quitGame,'q')

    rooms = {
        Rooms.PLANECRASH: RoomPlaneCrash("Plane crash")
        , Rooms.VILLAGE: RoomVillage("Village")
        , Rooms.CROSSROADS: RoomCrossroads("Crossroads")
        , Rooms.LIGHTHOUSE: RoomLighthouse("Lighthouse")
        , Rooms.BEACH: RoomBeach("Beach")
        , Rooms.CAVEENTRANCE: RoomCaveEntrance("Cave Entrance")
        , Rooms.CAVEINSIDE: RoomCaveInside("Inside Cave")
        , Rooms.CAVEEXIT: RoomCaveExit("Cave Exit")
        , Rooms.CLIFFS: RoomCliffs("Cliffs")
        , Rooms.FOREST: RoomForest("Forest")
        , Rooms.VILLAGEINSIDE: RoomVillageInside("Inside the village")
        , Rooms.CASTLEINSIDE: RoomCastleInside("Inside the village")
        , Rooms.LABORATORYINSIDE: RoomLaboratoryInside("Inside the village")
    }
    
    gameState = GameState(inp, timer, rooms, quitGame, lock)

    for key, room in rooms.items():
        room.postInit(gameState)
        timer.registerTimeOfDayEvent(room.reEnterRoom)

    Monitor.clear()
    print("\x1b[?25l") #hide cursor
    #rooms[Rooms.PLANECRASH].enterRoom()
    rooms[Rooms.CAVEINSIDE].enterRoom()


    
if __name__ == '__main__':
    try:
        initGame()
    except KeyboardInterrupt:
        print("interrupt")
    

