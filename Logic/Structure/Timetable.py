from typing import List, Dict
from Logic.Compliance.Negative import CapacityInequality, Clash, ConsecutiveIncompliance
from Logic.Compliance.Positive import FreePeriod, FreeGroupPeriod, FreeRoomPeriod, FreeInstructorPeriod

from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Logic.DateTime.Week import Week
from Logic.Statistics.Costs.Cost import ConstraintSatisfaction, TotalConstraintCompliance
from Logic.Structure.Configuration import Configuration
from Logic.Structure.Session import Session


class Timetable:

    def __init__(self, configuration: Configuration, periods: List[DayTime],
                 sessions: List[Session], times: List[Time]):
        self.configuration: Configuration = configuration
        self.week: Week = self.configuration.week
        self.periods: List[DayTime] = periods
        self.sessions: List[Session] = sessions
        self.times: List[Time] = times
        self.loop_stats: dict

        self.soft_constraints: ConstraintSatisfaction = ConstraintSatisfaction()
        self.hard_constraints: ConstraintSatisfaction = ConstraintSatisfaction()
        self.total_constraint: TotalConstraintCompliance = TotalConstraintCompliance(self.hard_constraints, self.soft_constraints, 0)

        self.free_periods: Dict[str, List[FreePeriod]] = {
            "group": List[FreeGroupPeriod],
            "room": List[FreeRoomPeriod],
            "instructor": [FreeInstructorPeriod]
        }

        self.capacity_inequality: CapacityInequality

        self.consecutive_incompliance: Dict[str, ConsecutiveIncompliance] = {
            "group": ConsecutiveIncompliance,
            "room": ConsecutiveIncompliance,
            "instructor": ConsecutiveIncompliance
        }

        self.clashes: Dict[str, List[Clash]] = {
            "room": [],
            "group": [],
            "instructor": []
        }

        self.stats = {
            "rooms": {"clashes": 0, "free": 0},
            "groups": {"clashes": 0, "free": 0},
            "instructors": {"clashes": 0, "free": 0}
        }

    def FindSession(self, session_identifier: int) -> Session:
        """
        Find a specific Session given the sesssion id
        """

        for session in self.sessions:
            if session.identifier == session_identifier:
                return session

    def ReplaceSession(self, old_session: Session, new_session: Session):
        """
        This is to change a session from a previous state into a new updated one
        old session->new session
        """
        index = self.sessions.index(self.FindSession(old_session.identifier))
        self.sessions[index] = new_session

    @property
    def week(self):
        return self._week

    @week.setter
    def week(self, value):
        self._week = value

    @property
    def sessions(self):
        return self._sessions

    @sessions.setter
    def sessions(self, value):
        self._sessions = value

    @property
    def periods(self):
        return self._periods

    @periods.setter
    def periods(self, value):
        self._periods = value

    @property
    def rooms(self):
        return self._rooms

    @rooms.setter
    def rooms(self, value):
        self._rooms = value

    @property
    def students(self):
        return self._students

    @students.setter
    def students(self, value):
        self._students = value

    @property
    def instructors(self):
        return self._instructors

    @instructors.setter
    def instructors(self, value):
        self._instructors = value

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value



    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    def Output(self)->dict:
       
        sessions = []
        for session in self.sessions:
            clash_costs = {
                "room": session.clash_costs['room'].value,
                "instructor": session.clash_costs["instructor"].value,
                "group": session.clash_costs["group"].value
            }
            
            preference_compliance_cost = {
                "room": session.preference_compliance_cost["room"].value,
                "group": session.preference_compliance_cost["group"].value,
                "instructor": session.preference_compliance_cost["instructor"].value,
            }
            consecutive_cost = {
                "room": session.consecutive_cost["room"].value,
                "group": session.consecutive_cost["group"].value,
                "instructor": session.consecutive_cost["instructor"].value,
            }
            temp = {
                "session_id": session.identifier,
                "day": session.day.name,
                "time": repr(session.daytime.time),
                "room": session.resources['room'].identifier,
                "instructor": session.schedule.instructor.identifier,
                "group": session.schedule.group.identifier,
                "clash_costs": clash_costs,
                "room_capacity_cost": session.room_capacity_cost.value,
                "preference_compliance_cost": preference_compliance_cost,
                "consecutive_cost": consecutive_cost,
                "overall_cost": session.overall_cost.value,
                "hard_constraint": session.hard_constraint_satisfaction.total_cost.value,
                "soft_constraint": session.soft_constraint_satisfaction.total_cost.value
            }
            sessions.append(temp)
        
        result = {"institution_name": self.configuration.instiution_name,
                   "soft_constraints": self.soft_constraints.total_cost.value,
                   "hard_constraints": self.hard_constraints.total_cost.value,
                   "total_cost": self.total_constraint.value,
                   "statistics": self.stats,
                   "sessions": sessions}

        return result