import msvcrt
import threading
import time

class InputHandler(threading.Thread):
    keycodes = {"\\x1b":"esc"}
    
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name        
        self.observers = {}        
        
    def run(self):       
        print ("Starting " + self.name)
        while(self.running):
            time.sleep(0.1)
            if msvcrt.kbhit():
                key = str(msvcrt.getch())[1:].replace("'","")
                key = self.keycodes.get(key, key)
                key = key.lower()
                self.keypress(key)
        print ("Stopping " + self.name)

    def keypress(self, key):
        print(key)
        for o in self.observers.get(key, []):
            o()

    def registerObserver(self, observer, key):
        key = key.lower()
        self.observers.setdefault(key, []).append(observer)

    def removeObserver(self, observer, key):
        key = key.lower()
        self.observers.setdefault(key, []).remove(observer)

    def startListening(self):
        self.running = True
        self.start()

    def stopListening(self):
        self.running = False
