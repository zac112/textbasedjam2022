import time
import os

class Monitor:
    SLOW = 10
    MEDIUM = 100
    FAST = 1000
    INSTANT = -1
    """
    Prints the given text on the monitor
    text: the text to print
    speed: how many letters per second; see class attributes (optional)
    """
    @staticmethod
    def print(text :str, speed = INSTANT):
        if speed == Monitor.INSTANT: 
            Monitor.__instantPrint(text)
            return

        speed = max(10, speed)
        for c in text:
            time.sleep(1.0/speed)
            print(c, end="", flush=True)
        print('\n')

    @staticmethod
    def __instantPrint(text :str):
        print(text)

    @staticmethod
    def clear():
        os.system("cls")

    @staticmethod
    def clearLines(numLines=1):
        for i in range(numLines):
            print("\033[A{}\033[A".format(' '*os.get_terminal_size().columns))
