import time

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

    @staticmethod
    def __instantPrint(text :str):
        print(text)