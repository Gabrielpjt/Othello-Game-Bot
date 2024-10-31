import time

class Stoppage: 
    stop = False
    move = False

    def __init__(self) -> None:
        pass

    def startCount(self):
        time.sleep(5)
        self.stop = True


    def isStop(self):
        return self.stop or self.move 

    