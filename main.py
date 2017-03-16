#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
OpenAurora

This is an open-source remake of the existing game Aurora 4x created by Steve Walmsley.

author: Robert Howlett
"""

import math
import sys
import random
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtCore import *
from players import Human

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


class GameState:
    """This is a dummy class containing the entire game state"""
    def __init__(self):
        self.pieceList = []
        self.playerList = [Human()]
        self.test_render()
        #self.test_paint_performance()

    def partial_state(self, player):
        """This function returns the state known to the nth player"""
        assert(player < len(self.playerList))
        # TODO: implement
        return copy.deepcopy(self)

    def test_render(self):
        demo_posns = [1+2j, 4+5j, 3-1j]
        self.pieceList = [GamePiece(posn, 0.0) for posn in demo_posns]

    def test_paint_performance(self):
        demo_posns = [random.randrange(0, 400) + random.randrange(0, 400)*1j for _ in range(100000)]
        self.pieceList = [GamePiece(posn, 0.0) for posn in demo_posns]


class OpenAurora(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = GameState()
        self.p_state = self.state.partial_state(0)

        self.main_view = QTabWidget(self)
        self.setCentralWidget(self.main_view)

        self.MapTab = MapTab(self)
        self.main_view.addTab(self.MapTab, "Tactical View")
        self.DummyTab = QLabel("This is a dummy tab")
        self.DummyTab.setFocusPolicy(Qt.StrongFocus)
        self.main_view.addTab(self.DummyTab, "Dummy Tab")

        exit_action = QAction(QIcon('exit24.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)

        turn_action = QAction(QIcon('dummy.png'), 'End Turn', self)
        turn_action.setShortcut('Ctrl+N')
        turn_action.triggered.connect(self.end_turn)
        # Todo: add variable target turn lengths
        self.target_turn_length = 1

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)
        turn_menu = menubar.addMenu('&Turn')
        turn_menu.addAction(turn_action)

        self.resize(800, 600)
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
        self.setFocusPolicy(Qt.StrongFocus)

        self.cur_posn = 0+0j
        self.cur_scal = 100.0

        self.mapFrame = TacView(self, parent.p_state)

        turn_btn = QPushButton('Next turn', self)
        turn_btn.setToolTip('This ends the turn')
        turn_btn.resize(turn_btn.sizeHint())
        turn_btn.clicked.connect(parent.end_turn)

        self.x_label = QLabel('x_label')
        self.y_label = QLabel('y_label')
        self.s_label = QLabel('s_label')
        self.map_instructions = QLabel('Welcome to the game!\nUse the arrow keys to move around\nand +/- to scroll.')

        ctrl_panel = QVBoxLayout()
        ctrl_panel.addWidget(self.x_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.y_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.s_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.map_instructions, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(turn_btn, alignment=Qt.AlignHCenter)

        hbox = QHBoxLayout()

        hbox.addLayout(ctrl_panel)
        hbox.addWidget(self.mapFrame, stretch=1)

        self.setLayout(hbox)

        self.set_view(0+0j, 100.0)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.move_view(posn=1)

        elif key == Qt.Key_Right:
            self.move_view(posn=-1)

        elif key == Qt.Key_Up:
            self.move_view(posn=1j)

        elif key == Qt.Key_Down:
            self.move_view(posn=-1j)

        elif key == Qt.Key_Minus:
            self.move_view(scal=1/math.sqrt(2))

        elif key in [Qt.Key_Plus, Qt.Key_Equal]:
            self.move_view(scal=math.sqrt(2))

        else:
            super(MapTab, self).keyPressEvent(event)

    def set_view(self, posn, scal):
        """This function sets the view to some position and scale"""
        # Set new board position
        self.cur_posn = posn
        self.cur_scal = scal

        # Write to the labels in the control panel.
        self.x_label.setText('x={:4f}'.format(posn.real))
        self.y_label.setText('y={:4f}'.format(posn.imag))
        self.s_label.setText('scale={:4f}'.format(scal))

        # Trigger a paint event
        self.mapFrame.update()

    def move_view(self, posn=None, scal=None):
        """This function modifies the existing view by adding a new position and/or multiplying the scale."""
        new_posn = self.cur_posn if posn is None else self.cur_posn + posn
        new_scal = self.cur_scal if scal is None else self.cur_scal * scal
        self.set_view(new_posn, new_scal)


class TacView(QFrame):
    """This class is for rendering the positions of things on a tactical view"""
    def __init__(self, parent, state):
        super().__init__()

        self.par = parent
        self.state = state

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        painter.fillRect(0, 0, rect.right(), rect.bottom(), QColor(0x000000))

        for piece in self.state.pieceList:
            self.draw_ship(painter, (piece.start_position + self.par.cur_posn) * self.par.cur_scal)

    @staticmethod
    def draw_ship(painter, posn):
        color = QColor(0x6666CC)
        width = 10
        painter.fillRect(posn.real, posn.imag, width, width, color)

if __name__ == '__main__':
    app = QApplication([])
    OA = OpenAurora()
    sys.exit(app.exec_())
