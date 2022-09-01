from Logics.Clash.Cost.Cost import Cost
from Logics.Clash.Room import RoomClash
from Logics.FreePeriods.Room import FreeRoomPeriod
from Logics.Structure.Session import Session
from Objects.Physical.Rooms import Room



class RoomCalculator:
    """
     Each Room is to be given a calculator and then sessions will be added to the calculator and eventually
     calculate clash cost by taking 1/total_clashes *100 and any free periods the room might have

     RC will be identified with the group identifier
     """

    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)
        return inst

    def __init__(self, room: Room, daytimes: list):
        self.identifier = None
        self.daytimes = list
        self.holder = {}
        self.clashed = []
        self.clashed_identifiers = {}
        self.total_clashes = 0
        self.room_clashes = []

        self.no_of_free_periods = 0
        self.free_periods = []

        self.room = room
        self.daytimes = daytimes

        self.identifier = room.name
        self.Divide()

    def __del__(self):
        self.identifier = None
        self.daytimes = list
        self.holder = {}
        self.clashed = []
        self.clashed_identifiers = {}
        self.total_clashes = 0
        self.room_clashes = []
        self.clashed = []
        self.no_of_free_periods = 0
        self.free_periods = []

    def Divide(self):
        for daytime in self.daytimes:
            self.holder[daytime] = []
            self.clashed_identifiers[daytime] = []

    def AddSession(self, session: Session):
        if session.room.name == self.identifier:
            self.holder[session.daytime].append(session)

    def Populate(self):
        for key, value in self.holder.items():
            total = len(value)
            clashing_identifiers = self.ExtractIdentifiers(value)
            if total > 1:
                """Calculate Cost"""
                self.total_clashes += 1
                cost = Cost(1, total)
                self.room_clashes.append(RoomClash(self.room, key, clashing_identifiers))
                for session in value:
                    session.room_clash_cost = cost
                    session.room_clash_identifiers = clashing_identifiers
                    self.clashed.append(session)
            elif total < 1:
                self.free_periods.append(FreeRoomPeriod(self.room, key))
                self.no_of_free_periods += 1

    @staticmethod
    def ExtractIdentifiers(sessions: list):
        identifiers = []
        for session in sessions:
            identifiers.append(session.schedule.identifier)
        del sessions
        return identifiers
