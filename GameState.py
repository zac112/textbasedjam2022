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
        self._inventory = set()
        self.townattackListeners = []

        self._inputHandler.registerObserver(self._clock.advanceTime, 'a')

    def registerGlobalEvents(self):
        beastAttackTime = 540
        shipwreckTime = 720
        eagleArrives1 = 180
        eagleArrives2 = eagleArrives1+400
        islandWarning = 800
        islandSinks = 900
        
        globalEvents = [(self._rooms[Rooms.BEACH].shipwreck,shipwreckTime),
                        (self._rooms[Rooms.CLIFFS].shipwreck,shipwreckTime),
                        (self._rooms[Rooms.LIGHTHOUSE].eagleArrives,180),
                        (self._rooms[Rooms.LIGHTHOUSE].eagleArrives,180+400),
                        (lambda _:self.notifyTownAttacked(True),beastAttackTime),
                        (lambda _:self.notifyTownAttacked(False),beastAttackTime+60),
                        (lambda _:Monitor.print("The whole island begins to shake. Is will probably sink soon."),islandWarning),
                        (self.islandSinks,islandSinks)
                        ]
        for event in globalEvents:
            self.registerEvent(*event)

    def islandSinks(self, ticks):
        Monitor.print("An EARTHQUAKE!!",speed=Monitor.SLOW)
        Monitor.print("It's more than just an earthquake; the whole island is sinking!")
        Monitor.print("You drown.")
        self.gameEnd()
        
    def getRoom(self, room : Rooms) -> Rooms:
        if room not in self._rooms: raise Exception(f"Room {room} not in rooms!")
        return self._rooms[room]

    def updateKnowledge(self, knowledge : Knowledge):
        level = self.getKnowledgeLevelFor(knowledge.value[0])
        if level < knowledge.value[1]:
            self._knowledge[knowledge.value[0]] = knowledge.value[1]

    def fulfillsRequirements(self, requirements : list):
        return all(map(lambda a:self.fulfillsRequirement(a),requirements))
    
    def fulfillsRequirement(self, requirement: Knowledge):
        req,reqlev = requirement.value
        if req not in self._knowledge: return False
        
        return self.getKnowledgeLevelFor(req) >= reqlev

    def addItem(self, item : Items):
        self._inventory.add(item)
        if self.hasItem(Items.Sword) and self.hasItem(Items.Tear):
            Monitor.print("The sword and jewel begin to... flash?")
            Monitor.print("Both vanish for a brief moment, then a brilliant sword appears in your hand!")
            self.removeItem(Items.Sword)
            self.removeItem(Items.Tear)
            self._inventory.add(Items.SwordOfArariel)
    
    def tookAction(self, action : Actions): self._actions.add(action)
    def hasAction(self, action : Actions): return action in self._actions
    def hasActions(self, actions : list): return all(map(lambda a:self.hasAction(a),actions))    
    def removeItem(self, item : Items): self._inventory.remove(item)
    def hasItem(self, item : Items): return item in self._inventory
    def hasAnyItem(self, items): return any(map(lambda a:self.hasItem(a),items))
    def getTick(self): return self._clock.getTick()
    #Returns the current time as a tuple(day:int,GameTime)
    def getTime(self) -> tuple: return self._clock.getTime()
    def getTimeOfDay(self) -> GameTime: return self.getTime()[1]
    def getKnowledgeLevelFor(self, req: KnowledgeType): return self._knowledge.get(req, 0)
    
    def registerInput(self, observer, key :str): self._inputHandler.registerObserver(observer, key)
    def unregisterInput(self, observer, key :str): self._inputHandler.unregisterObserver(observer, key)
    def registerEvent(self, observer, tick): self._clock.registerEvent(observer, tick)
    def unregisterEvent(self, observer, tick): self._clock.unregisterEvent(observer, tick)

    def registerTownAttackListener(self,obs):
        self.townattackListeners.append(obs)
        
    def notifyTownAttacked(self, isAttacked):
        for obs in self.townattackListeners:
            obs(isAttacked)
    
