#!/usr/bin/python3
# -*- coding: utf-8 -*-
from messages import *


class Player:
    """This is a superclass for the user(s) and AI."""
    def __init__(self, IF):
        self.IF = IF

    def get_orders(self):
        return []


class Interface:
    """This is the interface between a player and the game"""
    def __init__(self, GM, this_player):
        self.__GM = GM
        self.wake = True
        self.messages = []
        self.orders = []
        self.wakeTime = -1

        # Only initialise the player after the interface is ready for them.
        self.__player = this_player(self)

    def get_state(self):
        """This fetches a partial state from the GM"""
        return self.__GM.state
