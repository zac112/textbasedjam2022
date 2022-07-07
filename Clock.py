from Enums import GameTime

import threading
import time

class Timer(threading.Thread):

    def __init__(self, threadID, name, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ticks = 0
        self.eventObservers = {}
        self.timeObservers = []
        self.lock = lock
        self.currentTime = GameTime.MIDNIGHT
        
    def run(self):       
        while(self.running):
            time.sleep(1)
            self.tick()
        
    def tick(self):
        self.ticks += 1
        time = self.getTime()
        if time[1] != self.currentTime:
            self.currentTime = time[1]
            with self.lock:
                [obs() for obs in self.timeObservers]
            

        
        if self.ticks in self.eventObservers:
            with self.lock:
                for obs in self.eventObservers[self.ticks]:                
                    obs(self.ticks)
            self.eventObservers.pop(self.ticks,None)

    def getTick(self):
        return self.ticks

    #Returns the current time as a tuple(day:int,GameTime)
    def getTime(self) -> tuple:
        tick = self.getTick()
        day = int(tick/360.0)+1
        tick = tick%360
        texts = [#(60,GameTime.MIDNIGHT),
                 (6,GameTime.MIDNIGHT),
                 (90,GameTime.DAWN),
                 (270,GameTime.NOON),
                 (300,GameTime.DUSK),
                 (360,GameTime.MIDNIGHT)]
        return (day,[t[1] for t in texts if tick<t[0]][0])
    
    def registerTimeOfDayEvent(self,observer):
        self.timeObservers.append(observer)
        
    def registerEvent(self, observer, tick):
        self.eventObservers.setdefault(tick,[]).append(observer)

    def unregisterEvent(self, observer, tick):
        try: self.eventObservers[tick].remove(observer)
        except: pass

    def startCounting(self):
        self.running = True
        self.start()

    def stopCounting(self):
        self.running = False
        self.eventObservers = {}
        self.timeObservers = []

