import sys
import threading
from PyQt4.QtCore import QPoint, pyqtSlot
from PyQt4.QtGui import *
from alarm import Alarm

class myWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.alarm = Alarm()

        ####Counter - a minute textbox and a seconds textbox
        self.minuteTextbox = QLineEdit()
        self.minuteTextbox.setReadOnly(True)
        self.secondTextbox = QLineEdit()
        self.secondTextbox.setReadOnly(True)
        counterLayout = QHBoxLayout()
        counterLayout.addWidget(self.minuteTextbox)
        counterLayout.addWidget(self.secondTextbox)

        #### Buttons -a start, pause and skip button
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startPushed)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.setDisabled(True)
        self.pauseButton.clicked.connect(self.pausePushed)

        self.skipButton = QPushButton("Skip")
        self.skipButton.clicked.connect(self.skipPushed)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addWidget(self.skipButton)

        #### Layout
        layout = QVBoxLayout()
        layout.addLayout(counterLayout)
        layout.addLayout(buttonLayout)

        self.window = QWidget()
        self.window.setLayout(layout)
        self.window.show()
        self.setCentralWidget(self.window)


    def setPomodoro(self, pomodoro):
        self.pomodoro = pomodoro

    @pyqtSlot()
    def startPushed(self):
        """On start we disable the start button, enable the pause button
        and start the pomodoro running"""
        self.startButton.setDisabled(True)
        self.pauseButton.setEnabled(True)
        self.pomodoro.start()

    @pyqtSlot()
    def pausePushed(self):
        """On start we disable the pause button, enable the start button
        and pause the pomodoro"""
        self.pauseButton.setDisabled(True)
        self.startButton.setEnabled(True)
        self.pomodoro.pause()

    @pyqtSlot()
    def skipPushed(self):
        """On skip we set the pomodoro to the beginning of the
        next time period and reset the interface"""
        self.pauseButton.setDisabled(True)
        self.startButton.setEnabled(True)
        self.pomodoro.skip()

    def updateUIOnFinish(self):
        self.minuteTextbox.setText(str(self.pomodoro.getCurrentMinutes()))
        self.secondTextbox.setText(str(self.pomodoro.getCurrentSeconds()))
        self.pauseButton.setDisabled(True)
        self.startButton.setEnabled(True)
        self.alarm.playAlarm()

    def updateUI(self):
        self.minuteTextbox.setText(str(self.pomodoro.getCurrentMinutes()))
        self.secondTextbox.setText(str(self.pomodoro.getCurrentSeconds()))


