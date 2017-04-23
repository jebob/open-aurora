#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
from playerInterface import Player, Interface


class Human(Player):
    """This player is a human. It stores messages for the player and returns a state"""
    pass


class DummyAI(Player):
    """This is a placeholder for the AI"""
    def __init__(self):
        self.Name = random.randint(1, 1000)
        print("Dummy AI {} reporting for duty.".format(self.Name))
