class Student:
    name = str
    course = str
    gender = str
    year = str

    def __init__(self, name: str, course: str, gender: str, year: int):
        self.name = name
        self.course = course
        self.gender = gender
        self.year = year

    def __str__(self):
        return f'Student->{self.name}: year {self.year}'

    def __repr__(self):
        return self


class Group:
    """
    A group of students means they belong to the same course and year
    """

    def __init__(self, title: str, year: int):
        self.total = 0
        self.students = []

        self.free_periods = []

        self.title = title
        self.year = year

    def __repr__(self):
        return self

    def __str__(self):
        return f'Group->{self.title} year {self.year}:{self.total} students'

    def AddStudent(self, student):
        self.students.append(student)
        self.total += 1

class NullGroup(Group):
    def __init__(self):
        self.title = None
        self.year = None