import math
eventQueue = []  # todo this properly later


class GamePiece:
    """"This is the parent of all classes that have a presence on the map."""
    detection_radius = 0  # by default things don't detect
    speed = 0  # by default things don't move

    def __init__(self, position, time):
        assert isinstance(position, complex)
        assert isinstance(time, float)
        self.start_position = position
        self.target_position = position
        self.start_time = time
        self.finish_time = time

    def go_to(self, target_position):
        """This tells the craft to travel to a location."""
        assert isinstance(target_position, complex)
        assert self.speed > 0
        self.target_position = target_position
        distance = abs(target_position-self.start_position)
        self.finish_time = self.start_time + distance/self.speed
        eventQueue.append({'type': 'move finished', 'time': self.finish_time, 'piece': self})

    def position(self, time):
        """returns the position at the given time"""
        if self.start_position == self.target_position:
            return self.start_position
        assert self.start_time <= time <= self.finish_time
        f = (time - self.start_time) / (self.finish_time - self.start_time)
        assert 0 <= f <= 1
        return self.start_position*(1-f)+self.target_position*f


class Ship(GamePiece):
    speed = 5
    detection_radius = 2
    target_position = None

"""
I have:
    start position
    end position
    speed
    detection radius

I want to write:
    function that returns current location


d = sqrt(x*x+y*y)
rate of change = 0.5*(2x*dx/dt + 2y*dy/dt)/sqrt(x*x+y*y)

"""
=======
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

This is a Tetris game clone.

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
import random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QPushButton, QAction, qApp, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QIcon


class GamePiece:
    detectRange = 0  # by default things don't detect
    speed = 0  # by default things don't move
    """"This is a thing class. It represents an object or coll"""
    def __init__(self, position):
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert all(isinstance(n, int) for n in position)
        self.position = position


class GameState:
    """This is a dummy class containing the entire game state"""
    def __init__(self):
        self.pieceList = []
        self.set_demo()

    def set_demo(self):
        demo_posns = [(1, 2), (4, 5), (3, -1)]
        self.pieceList = [GamePiece(posn) for posn in demo_posns]


class OpenAurora(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = GameState()

        self.maintab = MapTab(self)
        self.setCentralWidget(self.maintab)

        exit_action = QAction(QIcon('exit24.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)

        self.resize(300, 380)
        self.center()
        self.setWindowTitle('OpenAurora')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def end_turn(self):
        """This method ends the turn"""
        pass


class MapTab(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.mapFrame = TacView(parent.state)

        turn_btn = QPushButton('Next turn', self)
        turn_btn.setToolTip('This ends the turn')
        turn_btn.resize(turn_btn.sizeHint())
        turn_btn.clicked.connect(parent.end_turn)

        hbox = QHBoxLayout()

        hbox.addWidget(turn_btn)
        hbox.addWidget(self.mapFrame, stretch=1)

        self.setLayout(hbox)


class TacView(QFrame):
    """This class is for rendering the positions of things on a tactical view"""
    def __init__(self, state):
        super().__init__()

        self.curX = 0
        self.curY = 0
        self.curScale = 100.0

        self.state = state

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        painter.fillRect(0, 0, rect.right(), rect.bottom(), QColor(0x000000))

        for piece in self.state.pieceList:
            self.draw_ship(painter, piece.position[0] * self.curScale, piece.position[1] * self.curScale)
            pass

    @staticmethod
    def draw_ship(painter, x, y):
        color = QColor(0x6666CC)
        width = 10
        painter.fillRect(x, y, width, width, color)

if __name__ == '__main__':
    app = QApplication([])
    OA = OpenAurora()
    sys.exit(app.exec_())
