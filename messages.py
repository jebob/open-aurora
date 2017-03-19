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

# Todo: add more messages
