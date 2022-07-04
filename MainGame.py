from Clock import Timer
from InputHandler import InputHandler
from Room import *
from GameState import GameState
from Rooms import Rooms

import atexit
import os
import sys
import msvcrt
import time

class Obs:

    def tick(self, ticks):
        print(ticks)

    def handleK(self):
        print("K pressed")

    def handleY(self):
        print("Y pressed")

timer = Timer(0,"Clock")
inp = InputHandler(1,"Input")

def initGame():
    o = Obs()
    timer.startListening()
    timer.registerObserver(o.tick)
    
    inp.startListening()
    inp.registerObserver(quitGame,'esc')

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

    rooms[Rooms.PLANECRASH].enterRoom()

def quitGame():
    print("cleanup")
    timer.stopListening()
    inp.stopListening()
    time.sleep(1)
    sys.exit(0)
    
if __name__ == '__main__':
    try:
        initGame()
    except KeyboardInterrupt:
        print("interrupt")
    

