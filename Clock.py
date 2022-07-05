import threading
import time

class Timer(threading.Thread):

    ticks = 0
    observers = []
    
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ticks = 0
        self.observers = {}       
        
    def run(self):       
        print ("Starting " + self.name)
        self.running = True
        while(self.running):
            time.sleep(1)
            self.tick()
        print ("Stopping " + self.name)
        
    def tick(self):
        self.ticks += 1
        if self.ticks in self.observers:
            for obs in self.observers[self.ticks]:
                obs(self.ticks)
            
            self.observers.pop(self.ticks,None)

    def getTick(self):
        return self.ticks

    def registerEvent(self, observer, tick):
        self.observers.setdefault(tick,[]).append(observer)

    def unregisterEvent(self, observer, tick):
        try: self.observers[tick].remove(observer)
        except: pass

    def startCounting(self):
        self.running = True
        self.start()

    def stopCounting(self):
        self.running = False
        self.observers.clear()

