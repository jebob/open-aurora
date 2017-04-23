#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Player:
    """This is a superclass for the user(s) and AI."""
    def get_orders(self):
        return []


class Interface:
    """This is the interface between a player and the game"""
    def __init__(self, GM, this_player):
        self.__GM = GM
        self.__player = this_player
        self.wake = True

    def get_state(self):
        """This fetches the state from the GM"""
        return self.__GM.state

    def get_orders(self):
        """This polls the AI for orders"""
        orders = self.__player.get_orders()
        return orders
