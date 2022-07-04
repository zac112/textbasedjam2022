from Rooms import Rooms

import InputHandler
import Clock

class GameState:

    def __init__(self, inputHandler : InputHandler, clock : Clock, rooms : dict):
        self._clock = clock
        self._inputHandler = inputHandler
        self._rooms = rooms

    def registerInput(self, observer, key :str):
        self._inputHandler.registerObserver(observer, key)

    def unregisterInput(self, observer, key :str):
        self._inputHandler.unregisterObserver(observer, key)

    def registerTick(self, observer):
        self._clock.registerObserver(observer)

    def unregisterTick(self, observer):
        self._clock.unregisterObserver(observer)

    def getRoom(self, room : Rooms) -> Rooms:
        if room not in self._rooms: raise Exception(f"Room {room} not in rooms!")
        return self._rooms[room]

class WriteableGameState(GameState):

    def setInputListener(self, inputHandler : InputHandler):
        pass