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
        self.observers = []        
        
    def run(self):       
        print ("Starting " + self.name)
        self.running = True
        while(self.running):
            time.sleep(1)
            self.tick()
        print ("Stopping " + self.name)
        
    def tick(self):
        self.ticks += 1
        for o in self.observers:
            o(self.ticks)

    def getTick(self):
        return self.ticks

    def registerObserver(self, observer):
        self.observers.append(observer)

    def unregisterObserver(self, observer):
        self.observers.remove(observer)

    def startCounting(self):
        self.running = True
        self.start()

    def stopCounting(self):
        self.running = False
        self.observers.clear()

