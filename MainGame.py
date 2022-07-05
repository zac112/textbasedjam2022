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
        , Rooms.CAVE: RoomCave("Cave")
        , Rooms.CAVEEXIT: RoomCaveExit("Cave Exit")
        , Rooms.CLIFFS: RoomCliffs("Cliffs")
        , Rooms.FOREST: RoomForest("Forest")
    }     

    gameState = GameState(inp, timer, rooms, quitGame)

    for key, room in rooms.items():
        room.postInit(gameState)
        timer.registerTimeOfDayEvent(room.reEnterRoom)

    Monitor.clear()
    rooms[Rooms.PLANECRASH].enterRoom()


    
if __name__ == '__main__':
    try:
        initGame()
    except KeyboardInterrupt:
        print("interrupt")
    

