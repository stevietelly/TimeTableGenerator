from Logics.Clash.Cost.Cost import Cost
from Logics.Clash.Instructor import InstructorClash
from Logics.FreePeriods.Instructor import FreeInstructorPeriod
from Logics.Structure.Session import Session
from Objects.Persons.Instructor import Instructor


class InstructorCalculator:
    """
    Each Instructor is to be given a calculator and then sessions will be added to the calculator and eventually
    calculate clash cost by taking 1/total_clashes *100

    ICC will be identified with the instructor Identifier
    """

    def __init__(self, instructor: Instructor, daytimes: list):
        self.holder = {}
        self.clashed = []
        self.clashed_identifiers = {}
        self.total_clashes = 0

        self.no_of_free_periods = 0
        self.free_periods = []

        self.instructor_clashes = []

        self.instructor = instructor
        self.daytimes = daytimes

        self.identifier = instructor.identifier
        self.Divide()

    def Divide(self):
        for daytime in self.daytimes:
            self.holder[daytime] = []
            self.clashed_identifiers[daytime] = []

    def AddSession(self, session: Session):
        if session.schedule.instructor.identifier == self.identifier:
            self.holder[session.daytime].append(session)

    def Populate(self):
        for key, value in self.holder.items():
            total = len(value)
            clashing_identifiers = self.ExtractIdentifiers(value)
            if total > 1:
                """Calculate Cost"""
                self.total_clashes += 1
                cost = Cost(1, total)
                self.instructor_clashes.append(InstructorClash(self.instructor, key, clashing_identifiers))
                for session in value:
                    session.instructor_clash_cost = cost
                    session.instructor_clash_identifiers = clashing_identifiers
                    self.clashed.append(session)
            elif total < 1:
                self.free_periods.append(FreeInstructorPeriod(self.instructor, key))
                self.no_of_free_periods += 1

    @staticmethod
    def ExtractIdentifiers(sessions: list):
        identifiers = []
        for session in sessions:
            identifiers.append(session.schedule.identifier)
        del sessions
        return identifiers
