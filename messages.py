#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Message:
    """This is a superclass for messages."""
    def __init__(self, time):
        self.time = time
        self.text = "default text"


class TimePassMess(Message):
    """This message is passed to every player on their turn to let them know how much time has passed"""
    def __init__(self, time):
        super().__init__(time)
        self.text = "The time is {}".format(time)
    pass


class ChatMess(Message):
    """This message is passed to a player if they receive a message from another player"""
    def __init__(self, time, text):
        super().__init__(time)
        self.text = "{}: {}".format(time, text)


# Todo: add more messages


class Order:
    """This is a superclass for orders to the GM"""
    pass


class WaitOrder(Order):
    """This is a request for control to be returned at a particular time"""
    def __init__(self, time):
        self.time = time


class ChatOrder(Order):
    """This is a message to all"""
    def __init__(self, text):
        self.text = text
