import time
import os
import sys
import threading
import re


class Monitor(threading.Thread):
    SLOW = 10
    MEDIUM = 100
    FAST = 1000
    INSTANT = 1

    WIDTH = 60
    HEIGHT = 30
    
    pos = [0,0]
    readingSpeed=30.0
    
    """
    Prints the given text on the monitor
    text: the text to print
    speed: how many letters per second; see class attributes (optional)
    """
    @staticmethod
    def print(text: str, pos: tuple = None, speed = INSTANT, delay=True, printline=True):        
        
        Monitor.dirty = True
        if pos:
            oldPos = Monitor.pos
            Monitor.setCursorPos(pos)

        if speed == Monitor.INSTANT:
            sleepFor = 0
        else:
            sleepFor = 1.0/speed

        for char in text:
            x,y = Monitor.pos
            if char=="\n":
                Monitor.printLine()
                continue
            if char=="\r":
                Monitor.pos[0]=0
                continue
            if char=="\t":
                raise Exception("Tabs are forbidden.")

            
            Monitor.buffer[y][x] = char
            Monitor.addX(1)
                                      
        if printline:
            Monitor.printLine()
        
        if pos:
            Monitor.setCursorPos(oldPos)

    @staticmethod
    def readableLine(text,speed=INSTANT,printline=True):
        input(text)
        Monitor.print("",printline=printline)
        
    @staticmethod
    def printLine():
        Monitor.addY(1)
        Monitor.pos[0]=0

    @staticmethod
    def clear():
        Monitor.dirty = True
        Monitor.buffer=[[' ']*Monitor.WIDTH for i in range(Monitor.HEIGHT)]
        Monitor.setCursorPos((0,0))

    #Clears lines from current position upwards
    #does not wrap
    @staticmethod
    def clearLines(numLines=1):
        for delta in range(numLines):
            for y,line in enumerate(Monitor.buffer):
                Monitor.buffer[y] = [' ']*Monitor.WIDTH
        Monitor.addY(max(-numLines+1,0))
            
        
    @staticmethod
    def getCursorPos():
        return Monitor.pos
    
    @staticmethod
    def setCursorPos(pos):
        Monitor.pos[0]=pos[0]
        Monitor.pos[1]=pos[1]

    @staticmethod
    def addX(amount):
        pos = Monitor.pos
        pos[0] = max(pos[0]+amount,0)
        if pos[0] >= Monitor.WIDTH:
            pos[0]=0
            Monitor.addY(1)
        
    
    @staticmethod        
    def addY(amount):
        pos = Monitor.pos
        pos[1]=max(pos[1]+amount,0)
        if pos[1] >= Monitor.HEIGHT:
            pos[1]=0
            
    @staticmethod
    def draw(text, pos:tuple=None, printline=False):        
        Monitor.print(text,pos=pos,printline=printline)

    def __init__(self, threadID, name, lock ):
        import random
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name   
        self.lock = lock
        Monitor.buffer=[[' ']*Monitor.WIDTH for i in range(Monitor.HEIGHT)]
        Monitor.dirty = True
        
    def run(self):
        os.system("cls") #enable ANSI codes
        print("\x1b[?25l") #hide cursor
        os.system(f"mode {Monitor.WIDTH},{Monitor.HEIGHT}")            
        while(self.running):                        
            time.sleep(0.1)
            if not Monitor.dirty:
                continue

            self.lock.acquire()
            print("\033[H",end="")                     
            for line in Monitor.buffer:
                print("".join(line),end="",flush=False)
            self.lock.release()
            print(end="",flush=True)
            
            Monitor.dirty = False

    def startDrawing(self):
        self.running=True
        self.start()
        

    def stopDrawing(self):
        self.running=False

