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

def quitGame(status : GameEnd):
    if status == GameEnd.LOSE:
        print("Game over.")
    if status == GameEnd.WIN:
        print("Congratulations! You beat the game!")
    timer.stopCounting()
    inp.stopListening()
    input("<Press enter to quit>")
    sys.exit(0)
    
def initGame():
    timer.startCounting()    
    inp.startListening()
    inp.registerObserver(lambda:quitGame(GameEnd.QUIT),'q')
    inp.registerObserver(lambda:quitGame(GameEnd.QUIT),'Q')

    gameState = GameState(inp, timer, quitGame, lock)
    for entry in Rooms:
        #a bit of eval-magic to workaround the circular import
        room = eval(entry.value)
        gameState._rooms[entry]=room
        room.postInit(gameState)
        if room._shouldDisplayApproximateTime():
            timer.registerTimeOfDayEvent(room.reEnterRoom)

    gameState.registerGlobalEvents()

    Monitor.clear()
    print("\x1b[?25l") #hide cursor
        
    gameState._rooms[Rooms.MAINMENU].enterRoom()


    
if __name__ == '__main__':
    try:
        initGame()
    except KeyboardInterrupt:
        print("interrupt")
    

