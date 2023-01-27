from Assets.DateTime.DayTime import DayTime
from Logics.Clash.Cost.Cost import Cost
from Logics.Structure.Schedule import Schedule


class Session:
    """
   Takes a Schedule class(group) day and time
   """
    room_clash_cost = Cost
    room_clash_identifiers = []

    group_clash_cost = Cost
    group_clash_identifiers = []

    instructor_clash_cost = Cost
    instructor_clash_identifiers = []

    def __init__(self, room, daytime: DayTime, schedule: Schedule):
        self.room = room
        self.schedule = schedule
        self.daytime = daytime
        self.day = self.daytime.day
        self.time = self.daytime.time

    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.schedule.unit.title} at {self.daytime} in {self.room.name}'
