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
    def __init__(self, identifier: int, unit: Unit, group: Group, instructor: Instructor):
        self.identifier: int = identifier
        self.unit: Unit = unit
        self.group: Group = group
        self.instructor: Instructor = instructor

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.identifier}'
    
    def __eq__(self, schedule):
        return (self.group == schedule.group) and (self.unit == schedule.unit) and (self.instructor == schedule.instructor) and (self.identifier == schedule.identifier) 
    
    def __ne__(self, schedule):
        return (self.group != schedule.group) and (self.unit != schedule.unit) and (self.instructor != schedule.instructor) and (self.identifier != schedule.identifier) 
