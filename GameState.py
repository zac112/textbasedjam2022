from Enums import *

import InputHandler
import Clock

class GameState:

    def __init__(self,
                 inputHandler : InputHandler,
                 clock : Clock,
                 gameEndCallback,
                 lock):
        self._clock = clock
        self._inputHandler = inputHandler
        self._rooms = {}
        #Callback ends the game
        self.endGame = gameEndCallback
        #Knowledgetype -> level
        self._knowledge = {}
        self._actions = set()
        self.lock = lock

    def registerGlobalEvents(self):
        globalEvents = [(self._rooms[Rooms.BEACH].shipwreck,360),
                        (self._rooms[Rooms.LIGHTHOUSE].eagleArrives,180),
                        (self._rooms[Rooms.SHOPKEEPERDIALOG].theBeastAttacks,10)
                        ]
        for event in globalEvents:
            self.registerEvent(*event)
        
    def getRoom(self, room : Rooms) -> Rooms:
        if room not in self._rooms: raise Exception(f"Room {room} not in rooms!")
        return self._rooms[room]

    def updateKnowledge(self, knowledge : Knowledge):
        level = self.getKnowledgeLevelFor(knowledge.value[0])
        if level < knowledge.value[1]:
            self._knowledge[knowledge.value[0]] = knowledge.value[1]

    def fulfillsRequirement(self, requirement: Knowledge):
        req,reqlev = requirement.value
        if req not in self._knowledge: return False
        
        return self.getKnowledgeLevelFor(req) >= reqlev

    def tookAction(self, action : Actions): self._actions.add(action)
    def hasAction(self, action : Actions): return action in self._actions
    def addItem(self, item : Items): self._inventory.add(item)
    def removeItem(self, item : Items): self._inventory.remove(item)
    def hasItem(self, item : Item): return item in self._inventory
    def getTick(self): return self._clock.getTick()
    #Returns the current time as a tuple(day:int,GameTime)
    def getTime(self) -> tuple: return self._clock.getTime()
    def getTimeOfDay(self) -> GameTime: return self.getTime()[1]
    def getKnowledgeLevelFor(self, req: KnowledgeType): return self._knowledge.get(req, 0)
    
    def registerInput(self, observer, key :str): self._inputHandler.registerObserver(observer, key)
    def unregisterInput(self, observer, key :str): self._inputHandler.unregisterObserver(observer, key)
    def registerEvent(self, observer, tick): self._clock.registerEvent(observer, tick)
    def unregisterEvent(self, observer, tick): self._clock.unregisterEvent(observer, tick)
