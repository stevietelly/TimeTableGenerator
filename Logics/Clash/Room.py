from Assets.DateTime.DayTime import DayTime
from Objects.Physical.Rooms import Room


class RoomClash:
    def __init__(self, room: Room, daytime: DayTime, clashed_session_identifiers: list):
        self.room = room
        self.daytime = daytime
        self.clashed_session_id = clashed_session_identifiers

        self.identifier = room.name
