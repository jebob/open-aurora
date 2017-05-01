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
from playerInterface import Interface
from players import Human, DummyAI
from characters import Character
from messages import *

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


class GameMaster:
    """This class controls the game flow."""
    human_ID = 0

    def __init__(self):
        # Initialise a state
        self.state = GameState()
        self.state.test_render()

        # Initialise player list
        # Populate with dummies, connect to the character list
        self.playerList = [Interface(self, DummyAI) for _ in self.state.characterList]

        # Now overwrite with the human player
        self.human_interface = Interface(self, Human)
        self.playerList[self.human_ID] = self.human_interface

    def main_loop(self):
        """Main game 'loop'.
        Due to not wanting to multithread and QT needing to be the main
        loop, the main game loop needs to be escapable.
        The nice thing about this design is that we can replace it with proper concurrency later.
        """
        # Load user commands into user's player
        self.human_interface.wake = False

        # Do a loop
        while True:
            # Fetch orders from all players
            orders = []
            for interface in self.playerList:
                orders.extend(interface.orders)
                interface.orders = []

            # Process orders
            for odr in orders:
                if isinstance(odr, ChatOrder):
                    # Pass messages to all players
                    msg = ChatMess(self.state.time, odr.text)
                    for interface in self.playerList:
                        interface.messages.append(msg)

            # Advance time

            # Identify reacting players

            # Pass responses to reacting players

            # Break if user's turn
            break

        # Possibly do some extra stuff to the user's player here.


class GameState:
    """This is a partial or complete game state"""
    def __init__(self):
        self.pieceList = []
        self.characterList = []
        self.time = 0.0

    def test_render(self):
        """This is a demo configuration"""
        demo_posns = [1+2j, 4+5j, 3-1j]
        self.pieceList = [GamePiece(posn, 0.0) for posn in demo_posns]
        self.characterList = [Character(), Character()]

    def test_paint_performance(self):
        """This is a demo configuration"""
        demo_posns = [random.randrange(0, 400) + random.randrange(0, 400)*1j for _ in range(100000)]
        self.pieceList = [GamePiece(posn, 0.0) for posn in demo_posns]


class OpenAurora(QMainWindow):
    def __init__(self, GM):
        super().__init__()

        self.GM = GM
        self.IF = self.GM.human_interface
        self.state = self.IF.get_state()

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

        # Advance time here.

        self.resize(800, 600)
        self.center()
        self.setWindowTitle('OpenAurora')
        self.update_ui()  # This ensures that everything is initialised correctly
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def end_turn(self):
        """This method ends the turn and updates the UI accordingly."""
        increment = self.target_turn_length

        self.IF.messages = []  # Flush old messages
        self.GM.main_loop()
        self.state = self.IF.get_state()
        # todo: implement a proper event displaying system (a tab?)
        for order in self.IF.messages:
            print(order.text)
        self.update_ui()

    def update_ui(self):
        self.MapTab.update_ui()


class MapTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.parent = parent

        self.cur_posn = 0+0j  # Define some initial view
        self.cur_scal = 100.0

        self.mapFrame = TacView(self, parent.state)

        turn_btn = QPushButton('Next turn', self)
        turn_btn.setToolTip('This ends the turn')
        turn_btn.resize(turn_btn.sizeHint())
        turn_btn.clicked.connect(parent.end_turn)

        self.x_label = QLabel('x_label')
        self.y_label = QLabel('y_label')
        self.s_label = QLabel('s_label')
        self.t_label = QLabel('t_label')  # Todo: ensure this is initialized properly
        self.map_instructions = QLabel('Welcome to the game!\nUse the arrow keys to move around\nand +/- to scroll.')

        ctrl_panel = QVBoxLayout()
        ctrl_panel.addWidget(self.x_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.y_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.s_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.t_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.map_instructions, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(turn_btn, alignment=Qt.AlignHCenter)

        hbox = QHBoxLayout()

        hbox.addLayout(ctrl_panel)
        hbox.addWidget(self.mapFrame, stretch=1)

        self.setLayout(hbox)
        self.update_ui()  # Finalise initialisation

    def keyPressEvent(self, event):
        # Todo: implement movement adjustments relative to the screen size e.g. up means 1/3 height upwards.
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

    def update_ui(self):
        """This function updates this tab"""
        # Write to the labels in the control panel.
        self.x_label.setText('x={:4f}'.format(self.cur_posn.real))
        self.y_label.setText('y={:4f}'.format(self.cur_posn.imag))
        self.s_label.setText('scale={:4f}'.format(self.cur_scal))
        self.t_label.setText('time={:4f}'.format(self.parent.state.time))

        # No need to trigger a paint event, the above should cause QT to trigger one.

    def move_view(self, posn=None, scal=None):
        """This function modifies the existing view by adding a new position and/or multiplying the scale."""
        self.cur_posn = self.cur_posn if posn is None else self.cur_posn + posn
        self.cur_scal = self.cur_scal if scal is None else self.cur_scal * scal
        self.update_ui()


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
    # Load the game
    game_master = GameMaster()
    app = QApplication([])
    OA = OpenAurora(game_master)
    sys.exit(app.exec_())
