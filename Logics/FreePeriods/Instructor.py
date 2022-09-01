from Assets.DateTime.DayTime import DayTime
from Objects.Persons.Instructor import Instructor


class FreeInstructorPeriod:
    """
    A daytime in which a certain instructor has no groups to teach
    """
    def __init__(self, instructor: Instructor, daytime: DayTime):
        self.instructor = instructor
        self.daytime = daytime

    def __repr__(self):
        return self

    def __str__(self):
        return f'{str(self.instructor)} at {self.daytime}'
