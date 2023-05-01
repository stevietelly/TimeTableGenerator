from typing import Dict, Union
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Logic.DateTime.DayTime import DayTime
from Logic.Statistics.Costs import Cost
from Logic.Structure.Schedule import Schedule
from Objects.Physical.Rooms import Room


class Session:
    """
   Takes a Schedule class(group) day and time
   """
    def __init__(self, identifier: int, room: Room, daytime: DayTime, schedule: Schedule):
        self.identifier: int = identifier
        self.room = room
        self.schedule: Schedule = schedule
        self.daytime = daytime
        self.day = self.daytime.day
        self.time  = self.daytime.time

        self.resources = {
            "room": self.room,
            "group": self.schedule.group,
            "instructor": self.schedule.instructor
        }

        # Costs 
        self.clash_costs: Dict[str, Cost.ClashCost] = {
            "group": Cost.ClashCost(0),
            "instructor": Cost.ClashCost(0),
            "room": Cost.ClashCost(0)
        
        }

        self.room_capacity_cost: Cost.RoomCapacity

        self.preference_compliance_cost: Dict[str, Cost.PreferenceSatisfacionCost] = {
            "room": Cost.PreferenceSatisfacionCost(0, 0),
            "group": Cost.PreferenceSatisfacionCost(0, 0),
            "instructor": Cost.PreferenceSatisfacionCost(0, 0)
        }

        self.priority_satisfaction_cost: Cost()

        self.consecutive_cost: Dict[str, Cost.Consecutive] = {
            "room": Cost.Consecutive(),
            "group":  Cost.Consecutive(),
            "instructor":  Cost.Consecutive()
        }

        self.overall_cost: Cost = Cost.Cost(0, 0)

        self.hard_constraint_satisfaction: Cost.ConstraintSatisfaction = Cost.ConstraintSatisfaction()
        self.soft_constraint_satisfaction: Cost.ConstraintSatisfaction = Cost.ConstraintSatisfaction()




    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.schedule.unit.title} at {self.daytime} in {self.room.name}'
    
    def __eq__(self, session) -> bool:
        if isinstance(session, Session):
            return self.identifier == session.identifier
                
        return False
        
    def __ne__(self, session) -> bool:
        return self.identifier == session.identifier

        


