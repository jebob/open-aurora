#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Player:
    """This is a superclass for the user(s) and AI."""
    pass


class Interface:
    """This is the interface between a player and the game"""
    def __init__(self, GM, this_player):
        self.__GM = GM
        self.__player = this_player

    def get_state(self):
        """This fetches the state from the GM"""
        return self.__GM.state

    def end_turn(self, time):
        """This asks the GM to advance time somewhat"""
        # todo
        return self.__GM.state
