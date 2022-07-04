from Clock import Timer
from InputHandler import InputHandler
from Room import *
from GameState import GameState
import Rooms

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

    gameState = GameState(inp, timer)

    for room in Rooms:
        room.postInit(gameState)

    Rooms.PLANECRASH.enterRoom()

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
    

