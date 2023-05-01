import random
from Logic.Compliance.Positive import FreePeriod
from Logic.Structure.Session import Session
from Logic.Structure.Timetable import Timetable

class Annealing:
    def __init__(self, timetable: Timetable) -> None:
        self.timetable = timetable
        self.free_periods = self.timetable.free_periods
    
    def free_period(self, object_type_: str, identifier: int) -> FreePeriod:
        free_period_list = []
        for free_period in self.free_periods[object_type_]:
            if free_period.object_.identifier == identifier:
                free_period_list.append(free_period)

        choice = random.choice(free_period_list)
        self.free_periods[object_type_].remove(choice)
        return choice
 
    def Optimize(self):
        self.optimizingclashes()
    
    def Output(self) -> Timetable:
        return self.timetable

    def optimizingclashes(self):
        """
        This function takes all clashing objects and tries to solve them (optimizing all clashes)
        """
        for clashed_room in self.timetable.clashes["room"]:
            for index, session in enumerate(clashed_room.sessions_holder):
                original_session: Session = self.timetable.FindSession(session.identifier)
                if index != 0:
                    free_room_period = self.free_period("room", clashed_room.object_.identifier)
                    mutated_session = original_session
                    mutated_session.room = free_room_period.object_
                    mutated_session.daytime = free_room_period.daytime
                    mutated_session.time = free_room_period.daytime.time
                    mutated_session.day = free_room_period.daytime.day
                    self.timetable.ReplaceSession(original_session, mutated_session)

        for clashed_group in self.timetable.clashes["group"]:
            for index, session in enumerate(clashed_group.sessions_holder):
                original_session: Session = self.timetable.FindSession(session.identifier)
                if index != 0:
                    free_group_period = self.free_period("group", clashed_group.object_.identifier)
                    mutated_session = original_session
                    mutated_session.daytime = free_group_period.daytime
        
                    self.timetable.ReplaceSession(original_session, mutated_session)

        for clashed_instructor in self.timetable.clashes["instructor"]:
            for index, session in enumerate(clashed_instructor.sessions_holder):
                original_session: Session = self.timetable.FindSession(session.identifier)
                if index != 0:
                    free_instructor_period = self.free_period("instructor", clashed_instructor.object_.identifier)
                    mutated_session = original_session
                    mutated_session.daytime = free_instructor_period.daytime
              
                    self.timetable.ReplaceSession(original_session, mutated_session)