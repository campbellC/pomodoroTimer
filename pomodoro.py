import threading
from secondTimer import SecondTimer

class Pomodoro:
    def __init__(self, pomodoroLength=25, shortRestLength=5, longRestLength=15):
        self.pomodoroNumber = 0
        self.pomodoroLength = pomodoroLength
        self.shortRestLength = shortRestLength
        self.longRestLength = longRestLength
        self.currentTimeLeft = pomodoroLength * 60 # time is in minutes, convert to seconds

        self.secondTimerStopFlag = None #set this to stop secondTimer
        self.secondTimer = None #This will fire every second
        self.UIlock = threading.Lock()

    def getCurrentSeconds(self):
        return self.currentTimeLeft % 60

    def getCurrentMinutes(self):
        return self.currentTimeLeft // 60

    def start(self):
        """To start the Pomodoro you start a thread that fires every second and
        reduces the currentTimeLeft by one each time"""
        self.secondTimerStopFlag = threading.Event()
        self.secondTimer = SecondTimer(self.secondTimerStopFlag, self.clockTick)
        self.secondTimer.daemon = True
        self.secondTimer.start()

    def finished(self):
        """To finish a time period we stop the timer and increase the current
        Pomodoro by one"""
        if self.secondTimer is not None:
            self.secondTimerStopFlag.set()
        self.pomodoroNumber += 1
        self.pomodoroNumber = self.pomodoroNumber % 8
        self.currentTimeLeft = self.getNextPomodoroLength()
        with self.UIlock:
            self.view.updateUIOnFinish()

    def clockTick(self):
        """This is called by the timer once a second. It reduces self.currentTimeLeft
        by one or moves to next pomdoro if this is the last second of the period"""
        self.currentTimeLeft -= 1
        if self.currentTimeLeft == 0:
            self.finished()
        else:
            with self.UIlock:
                self.view.updateUI()

    def pause(self):
        self.secondTimerStopFlag.set()
        with self.UIlock:
            self.view.updateUI()

    def skip(self):
        self.finished()

    def setView(self, view):
        self.view = view

    def getNextPomodoroLength(self):
        if self.pomodoroNumber % 2 == 0:
            temp = self.pomodoroLength
        elif self.pomodoroNumber % 7 == 0:
            temp = self.longRestLength
        else:
            temp = self.shortRestLength
        return temp * 60

