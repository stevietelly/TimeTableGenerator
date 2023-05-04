from Objects.User.Preferences.Preference import Preferences
from typing import List

class Unit:
    title = str
    sessions = int
    qualified_instructors = list

    def __init__(self,identifier: int, title: str, no_of_sessions: int, qualified_instructors: List[int]):
        self.identifier = identifier
        self.title = title
        self.sessions = no_of_sessions
        self.qualified_instructors = qualified_instructors

        self.preferences: Preferences
    
    @property
    def preferences(self):
        return self._preferences
    
    @preferences.setter
    def preferences(self, value):
        self._preferences = value

    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.title} {self.sessions} in a week'

    def __eq__(self, unit) -> bool:
        return (self.title == unit.title) and (self.sessions == unit.sessions)

    def __ne__(self, unit) -> bool:
        return (self.title != unit.title) or (self.sessions != unit.sessions)

