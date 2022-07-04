import msvcrt
import threading
import time

class InputHandler(threading.Thread):
    keycodes = {
        "\\x1b":"esc"
        ,"\\xe0H":'up'
        ,"\\xe0M":'right'
        ,"\\xe0P":'down'
        ,"\\xe0K":'left'
        ,"\\r":'enter'
    }
    
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name        
        self.observers = {}        
        
    def trimKey(self, keycode):
        return str(keycode)[1:].replace("'","")

    def run(self):       
        print ("Starting " + self.name)
        while(self.running):
            if msvcrt.kbhit():
                key = self.trimKey(msvcrt.getch())
                if key =="\\xe0": key += self.trimKey(msvcrt.getch())
                key = self.keycodes.get(key, key)
                key = key.lower()
                self.keypress(key)
        print ("Stopping " + self.name)

    def keypress(self, key):
        #print(key)
        for o in self.observers.get(key, []):
            o()

    def registerObserver(self, observer, key):
        key = key.lower()
        self.observers.setdefault(key, []).append(observer)

    def unregisterObserver(self, observer, key):
        key = key.lower()
        self.observers.setdefault(key, []).remove(observer)

    def startListening(self):
        self.running = True
        self.start()

    def stopListening(self):
        self.running = False
        self.observers.clear()
