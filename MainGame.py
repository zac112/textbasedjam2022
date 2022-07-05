from Clock import Timer
from InputHandler import InputHandler
from Room import *
from GameState import GameState
from Rooms import Rooms
from Monitor import Monitor
from threading import Lock

import sys
import time

lock = Lock()
timer = Timer(0,"Clock", lock)
inp = InputHandler(1,"Input", lock)

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
        , Rooms.CAVE: RoomCave("Cave")
        , Rooms.CAVEEXIT: RoomCaveExit("Cave Exit")
        , Rooms.CLIFFS: RoomCliffs("Cliffs")
        , Rooms.FOREST: RoomForest("Forest")
    }     

    gameState = GameState(inp, timer, rooms)

    for key, room in rooms.items():
        room.postInit(gameState)

    Monitor.clear()
    rooms[Rooms.PLANECRASH].enterRoom()

def quitGame():
    print("cleanup")
    timer.stopCounting()
    inp.stopListening()
    time.sleep(1)
    sys.exit(0)
    
if __name__ == '__main__':
    try:
        initGame()
    except KeyboardInterrupt:
        print("interrupt")
    

