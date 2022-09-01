from Logics.Clash.Cost.Cost import Cost
from Logics.Clash.Group import GroupClash
from Logics.FreePeriods.Group import FreeGroupPeriod
from Logics.Structure.Session import Session
from Objects.Persons.Students import Group


class GroupCalculator:
    """
     Each Group is to be given a calculator and then sessions will be added to the calculator and eventually
     calculate clash cost by taking 1/total_clashes *100 and any free periods the group might have

     GCC will be identified with the group Title and year
     """

    def __init__(self, group: Group, daytimes: list):
        self.holder = {}
        self.clashed = []
        self.clashed_identifiers = {}
        self.total_clashes = 0

        self.no_of_free_periods = 0
        self.free_periods = []

        self.group_clashes = []

        self.group = group
        self.daytimes = daytimes

        self.identifier = str(group)
        self.Divide()

    def Divide(self):
        for daytime in self.daytimes:
            self.holder[daytime] = []
            self.clashed_identifiers[daytime] = []

    def AddSession(self, session: Session):
        if str(session.schedule.group) == self.identifier:
            self.holder[session.daytime].append(session)

    def Populate(self):
        for key, value in self.holder.items():
            total = len(value)
            clashing_identifiers = self.ExtractIdentifiers(value)
            if total > 1:
                """Calculate Cost"""
                self.total_clashes += 1
                cost = Cost(1, total)
                self.group_clashes.append(GroupClash(self.group, key, clashing_identifiers))
                for session in value:
                    session.group_clash_cost = cost
                    session.group_clash_identifiers = clashing_identifiers
                    self.clashed.append(session)
            elif total < 1:
                self.free_periods.append(FreeGroupPeriod(self.group, key))
                self.no_of_free_periods += 1

    @staticmethod
    def ExtractIdentifiers(sessions: list):
        identifiers = []
        for session in sessions:
            identifiers.append(session.schedule.identifier)
        del sessions
        return identifiers
