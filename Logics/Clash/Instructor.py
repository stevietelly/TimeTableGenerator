from Assets.DateTime.DayTime import DayTime
from Objects.Persons.Instructor import Instructor


class InstructorClash:
    def __init__(self, instructor: Instructor, daytime: DayTime, clashed_session_identifiers: list):
        self.instructor = instructor
        self.daytime = daytime
        self.clashed_session_id = clashed_session_identifiers

        self.identifier = instructor.name
