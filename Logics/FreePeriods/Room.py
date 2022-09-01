from Assets.DateTime.DayTime import DayTime
from Objects.Physical.Rooms import Room


class FreeRoomPeriod:
    """
    A daytime in which a certain room has no group in it
    """
    def __init__(self, room: Room, daytime: DayTime):
        self.room = room
        self.daytime = daytime

    def __repr__(self):
        return self

    def __str__(self):
        return f'{str(self.room)} at {self.daytime}'
