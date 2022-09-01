from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group


class Schedule:
    """
    A schedule is made of
    1. a group of students taking a unit
    2. Unit
    3. A specific Instructor chosen form one of the units instructors
    """
    instructor = Instructor
    group = Group
    unit = Unit
    identifier = int

    def __init__(self, identifier: int, unit: Unit, group: Group, instructor: Instructor):
        self.identifier = identifier
        self.unit = unit
        self.group = group
        self.instructor = instructor

    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.identifier}'
