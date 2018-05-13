#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
OpenAurora

This is an open-source remake of the existing game Aurora 4x created by Steve Walmsley.

author: Robert Howlett
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from playerInterface import Interface
from players import Human, DummyAI
from characters import Character
from messages import *
from tab import Tab
from tactical.tactical import Tactical

eventQueue = []  # todo this properly later




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
        self.state.tactical.test_render()

        # Initialise player list
        # Populate with dummies, connect to the character list
        self.playerList = [Interface(self, DummyAI) for _ in self.state.characterList]

        # Now overwrite with the human player
        self.human_interface = Interface(self, Human)
        try:
            self.playerList[self.human_ID] = self.human_interface
        except IndexError:
            # Hm, can't find human player
            pass

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


            # Decide on how far to advance
            timeIncrement = 1

            # Advance time
            self.state.time += timeIncrement

            # Identify reacting players

            # Pass responses to reacting players

            # Break if user's turn
            break

        # Possibly do some extra stuff to the user's player here.


class GameState:
    """This is a partial or complete game state"""
    def __init__(self):
        self.characterList = []
        self.time = 0.0
        self.tactical = Tactical(self)

    def get_tabs(self):
        tabs = dict()
        tabs.update(self.tactical.tabs)

        dummy_tab = Tab()
        dummy_tab.setFocusPolicy(Qt.StrongFocus)
        tabs.update({"Dummy Tab": dummy_tab})
        return tabs


class OpenAurora(QMainWindow):
    def __init__(self, GM):
        super().__init__()

        self.GM = GM
        self.IF = self.GM.human_interface
        self.state = self.IF.get_state()

        self.main_view = QTabWidget(self)
        self.setCentralWidget(self.main_view)

        for label, tab in self.state.get_tabs().items():
            self.main_view.addTab(tab, label)

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
        for tab in self.state.get_tabs().values():
            tab.update_ui()


if __name__ == '__main__':
    # Load the game
    app = QApplication([])
    game_master = GameMaster()
    OA = OpenAurora(game_master)
    sys.exit(app.exec_())
