class Unit:
    title = str
    sessions = int
    qualified_instructors = list

    def __init__(self, title: str, sessions: int, qualified_instructors: list):
        self.title = title
        self.sessions = sessions
        self.qualified_instructors = qualified_instructors

    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.title} {self.sessions} in a week'

class NullUnit(Unit):
    def __init__(self):
        self.title = None
        self.sessions = None
        self.qualified_instructors = None