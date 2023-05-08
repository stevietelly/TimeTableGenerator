import random
from Assets.Functions.Echo import Echo
from Logic.Compliance.Positive import FreePeriod
from Logic.Structure.Session import Session
from Logic.Structure.Timetable import Timetable


class ConstaraintSatisfaction:
    def __init__(self, timetable: Timetable) -> None:
        """
        This algorithim just goes through all clashes and 
        issues and tries to fix them as much as possible
        """
        self.timetable = timetable
        self.free_periods = timetable.free_periods
        self.clashes = timetable.clashes

        self.echo = Echo()
    
    def Optimize(self):
        self.optimizeClashes()
    
    def optimizeClashes(self):
        """
        This function takes all clashing objects and tries to solve them (optimizing all clashes)
        """
        self.echo.print("Constraint Satsifaction: Optimising All Clashes")

        self.optimizingRoomClashes()
        self.optimizingInstructorClashes()
        self.optimizingGroupClashes()
    
    def optimizingRoomClashes(self):
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

    def optimizingGroupClashes(self):
        for clashed_group in self.timetable.clashes["group"]:
            for index, session in enumerate(clashed_group.sessions_holder):
                original_session: Session = self.timetable.FindSession(session.identifier)
                if index != 0:
                    free_group_period = self.free_period("group", clashed_group.object_.identifier)
                    mutated_session = original_session
                    mutated_session.daytime = free_group_period.daytime
        
                    self.timetable.ReplaceSession(original_session, mutated_session)
    
    def optimizingInstructorClashes(self):        
        for clashed_instructor in self.timetable.clashes["instructor"]:
            for index, session in enumerate(clashed_instructor.sessions_holder):
                original_session: Session = self.timetable.FindSession(session.identifier)
                if index != 0:
                    free_instructor_period = self.free_period("instructor", clashed_instructor.object_.identifier)
                    mutated_session = original_session
                    mutated_session.daytime = free_instructor_period.daytime
                
                    self.timetable.ReplaceSession(original_session, mutated_session)

    def free_period(self, object_type_: str, identifier: int) -> FreePeriod:
        free_period_list = []
        for free_period in self.free_periods[object_type_]:
            if free_period.object_.identifier == identifier:
                free_period_list.append(free_period)

        choice = random.choice(free_period_list)
        # self.free_periods[object_type_].remove(choice)
        return choice
    
    def Output(self)->Timetable:
        return self.timetable