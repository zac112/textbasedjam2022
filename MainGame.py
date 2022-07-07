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

    rooms = {}    
    gameState = GameState(inp, timer, rooms, quitGame, lock)

    for entry in Rooms:
        #a bit of eval-magic to workaround the circular import
        room = eval(entry.value)
        rooms[entry]=room
        room.postInit(gameState)
        if room._shouldDisplayApproximateTime():
            timer.registerTimeOfDayEvent(room.reEnterRoom)
        for event in room.getGlobalEvents():
            timer.registerEvent(*event)

    Monitor.clear()
    print("\x1b[?25l") #hide cursor
    #rooms[Rooms.PLANECRASH].enterRoom()
    rooms[Rooms.CAVE1].enterRoom()


    
if __name__ == '__main__':
    try:
        initGame()
    except KeyboardInterrupt:
        print("interrupt")
    

