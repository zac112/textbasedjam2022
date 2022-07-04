import InputHandler
import Clock

class GameState:

    def __init__(self, inputHandler : InputHandler, clock : Clock):
        self._clock = clock
        self._inputHandler = inputHandler

    def registerInput(self, observer : function, key :str):
        self._inputHandler.registerObserver(observer, key)

    def unregisterInput(self, observer : function, key :str):
        self._inputHandler.unregisterObserver(observer, key)

    def registerTick(self, observer : function):
        self._clock.registerObserver(observer)

    def unregisterTick(self, observer : function):
        self._clock.unregisterObserver(observer)


class WriteableGameState(GameState):

    def setInputListener(self, inputHandler : InputHandler):
        pass