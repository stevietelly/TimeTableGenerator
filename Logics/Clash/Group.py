from Assets.DateTime.DayTime import DayTime
from Objects.Persons.Students import Group


class GroupClash:
    def __init__(self, group: Group, daytime: DayTime, clashed_session_identifiers: list):
        self.group = group
        self.daytime = daytime
        self.clashed_session_id = clashed_session_identifiers

        self.identifier = str(group)
