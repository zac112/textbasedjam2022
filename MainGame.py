from Clock import Timer
from InputHandler import InputHandler
from Room import *

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
        "Plane crash": RoomPlaneCrash("Plane crash"),
        "Village": RoomVillage("Village"),
        "Crossroads": RoomCrossroads("Crossroads"),
        "Beach": RoomBeach("Beach"),
        "Cave Entrance": RoomCaveEntrance("Cave Entrance"),
        "Cave Exit": RoomCaveExit("Cave Exit"),
        "Cave": RoomCave("Cave"),
        "Cliffs": RoomCliffs("Cliffs"),
        "Forest": RoomForest("Forest")
    }

    gameState = {"Timer":timer, "InputHandler":inp, "Rooms": rooms}
    
    for name,room in rooms.items():
        room.postInit(gameState)
    rooms["Plane crash"].enterRoom()

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
    

