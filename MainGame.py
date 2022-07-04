from Clock import Timer
from InputHandler import InputHandler

import atexit
import os
import sys
import msvcrt

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
    inp.registerObserver(o.handleK,'k')
    inp.registerObserver(o.handleY,'y')

def quitGame():
    print("cleanup")
    timer.stopListening()
    inp.stopListening()
    sys.exit(0)
    
if __name__ == '__main__':
    try:
        initGame()
    except KeyboardInterrupt:
        print("interrupt")
    

