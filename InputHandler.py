import msvcrt
import threading
import time
import traceback

class InputHandler(threading.Thread):
    keycodes = {
        "\\x1b":"esc"
        ,"\\xe0H":'up'
        ,"\\xe0M":'right'
        ,"\\xe0P":'down'
        ,"\\xe0K":'left'
        ,"\\r":'enter'
    }
    
    def __init__(self, threadID, name, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name        
        self.observers = {}
        self.lock = lock
        
    def trimKey(self, keycode):
        return str(keycode)[1:].replace("'","")

    def run(self):       
        while(self.running):
            time.sleep(0.1)
            if msvcrt.kbhit():
                key = self.trimKey(msvcrt.getch())
                if key =="\\xe0": key += self.trimKey(msvcrt.getch())                
                key = self.keycodes.get(key, key)
                key = key.lower()
                self.keypress(key)

    def keypress(self, key):
        #print(key)
        self.lock.acquire()
        for obs in self.observers.get(key, []):
            try:
                obs()
            except Exception as e:
                with open("error.txt","w") as f:
                    traceback.print_exc(file=f)
                    print(e)
        self.lock.release()

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
        self.observers = {}
