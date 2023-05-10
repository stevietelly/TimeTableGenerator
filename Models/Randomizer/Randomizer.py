
import random
from typing import Union
from Logic.Structure.Session import Session
from Logic.Structure.Timetable import Timetable

class Randomizer:
    """
    A randomizer typically takes in a timetable and randomly changes
    attributes about it in no specific order, completely random chosen
    this is helpful when trying to bring in new attributes to the
    timetable to make it more optimised
    """
    def __init__(self, timetable: Timetable) -> None:
        self.timetable = timetable
        self.daytimes = timetable.periods
    
    def Random(self):
        for session in self.timetable.sessions:
            daytime = random.choice(self.daytimes)
            new_session: Session = session
            new_session.daytime = daytime
            self.timetable.ReplaceSession(session, new_session)
        return self.timetable
    
    def Output(self)-> Timetable:
        return self.timetable