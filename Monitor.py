import time
import os
import sys
from ctypes import wintypes
import ctypes
import re

class Monitor:
    SLOW = 10
    MEDIUM = 100
    FAST = 1000
    INSTANT = -1

    readingSpeed=30.0
    """
    Prints the given text on the monitor
    text: the text to print
    speed: how many letters per second; see class attributes (optional)
    """
    @staticmethod
    def print(text: str, pos: tuple = None, speed = INSTANT, delay=True, printline=True):
        if speed == Monitor.INSTANT: 
            Monitor.__instantPrint(text,delay=delay)
            return
        
        oldPos = Monitor.getCursorPos()
        if pos:
            Monitor.setCursorPos(pos[0],pos[1])
        
        speed = max(10, speed)
        for c in text:
            time.sleep(1.0/speed)
            print(c, end="", flush=True)

        if printline:print()
        
        if pos: Monitor.setCursorPos(oldpos[0],oldpos[1])

        if delay: time.sleep(len(text)/Monitor.readingSpeed)

    @staticmethod
    def printLine():
        Monitor.print("")

    @staticmethod
    def __instantPrint(text :str, delay: int=0):
        print(text)
        if delay: time.sleep(len(text)/Monitor.readingSpeed)
        print()

    @staticmethod
    def clear():
        os.system("cls")

    @staticmethod
    def clearLines(numLines=1):
        for i in range(numLines):
            Monitor.print("\033[A{}\033[A".format(' '*os.get_terminal_size().columns))
        
    @staticmethod
    def getCursorPos():
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

        try:
            _ = ""
            sys.stdout.write("\x1b[6n")
            #sys.stdout.write("")
            sys.stdout.flush()
            while not (_ := _ + sys.stdin.read(1)).endswith('R'): pass
            res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
        finally:            
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
            
        if(res):
            return (int(res.group("x")), int(res.group("y")))
        return (-1, -1)        

    @staticmethod
    def positionCursor(pos):
        if pos: return(f"\033[{pos[1]};{pos[0]}f")
        return ""
    
    @staticmethod
    def setCursorPos(pos):
        print(Monitor.positionCursor(pos))        

    @staticmethod
    def draw(text, pos:tuple=None, printline=False):
        print(f"{Monitor.positionCursor(pos)}{text}", end="", flush=True)
        
