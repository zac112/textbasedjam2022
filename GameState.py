from Rooms import Rooms
from Knowledge import *

import InputHandler
import Clock

class GameState:

    def __init__(self, inputHandler : InputHandler, clock : Clock, rooms : dict, gameEndCallback):
        self._clock = clock
        self._inputHandler = inputHandler
        self._rooms = rooms
        self.endGame = gameEndCallback
        #Knowledgetype -> level
        self._knowledge = {}

    def registerInput(self, observer, key :str):
        self._inputHandler.registerObserver(observer, key)

    def unregisterInput(self, observer, key :str):
        self._inputHandler.unregisterObserver(observer, key)

    def registerEvent(self, observer, tick):
        self._clock.registerEvent(observer, tick)

    def unregisterEvent(self, observer, tick):
        self._clock.unregisterEvent(observer, tick)

    def getTick(self):
        return self._clock.getTick()
    
    def getRoom(self, room : Rooms) -> Rooms:
        if room not in self._rooms: raise Exception(f"Room {room} not in rooms!")
        return self._rooms[room]

    def updateKnowledge(self, knowledge : Knowledge):
        level = self.getKnowledgeLevelFor(knowledge.value[0])
        if level < knowledge.value[1]:
            self._knowledge[knowledge.value[0]] = knowledge.value[1]

    def getKnowledgeLevelFor(self, knowledgeType : KnowledgeType) -> int:        
        return self._knowledge.get(knowledgeType, 0)
