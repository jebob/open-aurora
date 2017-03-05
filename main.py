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
