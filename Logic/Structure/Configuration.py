from Logic.DateTime.Time import Time
from typing import List, Dict, Union
from Logic.DateTime.Week import Week

from Objects.User.Priorities.Priorities import Priorities

class Configuration:
    def __init__(self, name:str, start_time: str, end_time: str, days: List[str]) -> None:
        self.instiution_name: str = name
        self.start_time = Time(start_time)
        self.end_time = Time(end_time)

        self.days = days
        self.week: Week 
        self.duration_per_session:int
        self.total_duration_for_sessions: int
        self.soft_constraints_satisfaction_rate:int
        
        self.consecutive: Dict[str, int] = {
            "room": int,
            "instructor": int,
            'group': int
        }

        self.system: Dict[str, Union[bool, int]] = {
            "limit": int,
            "saturation": bool,
            "tries": int
        }

        self.priorities: Priorities
