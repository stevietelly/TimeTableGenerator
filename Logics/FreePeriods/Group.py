from Assets.DateTime.DayTime import DayTime
from Objects.Persons.Students import Group


class FreeGroupPeriod:
    """
    A daytime in which a certain group has no group in it
    """
    def __init__(self, group: Group, daytime: DayTime):
        self.group = group
        self.daytime = daytime

    def __repr__(self):
        return self

    def __str__(self):
        return f'{str(self.group)} at {self.daytime}'
