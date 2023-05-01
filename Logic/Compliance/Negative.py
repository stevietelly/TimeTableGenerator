from typing import Union, List
from Logic.Compliance.Compliance import Compliance
from Logic.DateTime.DayTime import DayTime
from Logic.Structure.Session import Session
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room


class NegativeCompliance(Compliance):
    def __init__(self) -> None:
        super().__init__()
        self.compliance_type = "negative"

class UnAcceptedCapacity(NegativeCompliance):
    def __init__(self, object_: Room) -> None:
        super().__init__()
        self.room: Room = object_

class Clash(NegativeCompliance):
    def __init__(self, object_: Union[Group, Room, Instructor], daytime:DayTime) -> None:
        """
        A daytime in which a certain object has multiple sessions
        """
        super().__init__()
        self.daytime: DayTime = daytime
        self.object_: Union[Group, Room, Instructor] = object_
 
class GroupClash(Clash):
    def __init__(self, group: Group, daytime: DayTime) -> None:
        """
        A specific daytime when a group  has multiple sessions
        """
        super().__init__(group, daytime)

class RoomClash(Clash):
    def __init__(self, room: Room, daytime: DayTime) -> None:
        """
        A specific daytime when a room  has multiple sessions
        """
        super().__init__(room, daytime)

class InstructorClash(Clash):
    def __init__(self, instructor: Instructor, daytime: DayTime) -> None:
        """
        A specific daytime when an instructor  has multiple sessions
        """
        super().__init__(instructor, daytime)

class UnSatisfiedPreferences(NegativeCompliance):
    def __init__(self) -> None:
        super().__init__()

class CapacityInequality(NegativeCompliance):
    def __init__(self, room: Room) -> None:
        super().__init__()
        self.room = room

class ConsecutiveIncompliance(NegativeCompliance):
    def __init__(self) -> None:
        super().__init__()
        self.sessions_holder: List[List[Session]]
    
    def AddSession(self, sessions: List[Session]):
        return super().AddSession(sessions)