"""
The Evaluation Function
"""

import sys
from typing import Dict, List
from Assets.Functions.Echo import Echo
from Logic.Compliance.Negative import CapacityInequality, Clash
from Logic.Compliance.Positive import FreeGroupPeriod, FreeInstructorPeriod, FreePeriod, FreeRoomPeriod
from Logic.Statistics.Costs.Cost import ClassOnePrioritySatisfaction, ClassTwoPrioritySatisfaction, ConstraintSatisfaction, TotalConstraintCompliance
from Logic.Structure.Session import Session
from Objects.Persons.Instructor import Instructor
from Logic.Statistics.Calculators.Calculator import GroupCalculator, InstructorCalculator, RoomCalculator
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room
from Logic.Structure.Timetable import Timetable
from Objects.User.Priorities.Priorities import Priorities


class FitnessEvaluation:

    def __init__(self, timetable: Timetable, rooms: List[Room],
                 groups: List[Group], instructors: List[Instructor],
                 priorities: Priorities) -> None:
        self.rooms = rooms
        self.groups = groups
        self.instructors = instructors
        self.priorities: Priorities = priorities

    
        """"
        This function is used to get the fitness of a solution based on compliance with the constraints
        specified
        The following will be considered 

        1. Clash (which will take into consideration)
                Room-Clashes
                Instructor-Clashes
                Group-Clashes
        
        2. Room Capacity Adherence 
        3. Class one Priority Aherence (Level One and Level Two preferences)
        4. Total Session Adherence
        5. Instructor Qualification Adherence
        6. Prefered Instructor Adherence
        # FIXME: Preffered Instructor Adherence
        7. Class two Priority Aherence (Level Three and Level Four preferences)
        8. Consecetive Session Adherence

        Also in the process a free period analysis and clashing sessions analysis will be conducted

        param:

        """
        self.echo = Echo()
        self.timetable: Timetable = timetable
        self.room_holder = rooms
        self.group_holder = groups
        self.instructor_holder = instructors

        # Calculators
        self.group_calculator: List[GroupCalculator] = []
        self.instructor_calculator: List[InstructorCalculator] = []
        self.room_calculator: List[RoomCalculator] = []


        self.soft_constraint_satisfaction_acceptance: int =  timetable.configuration.soft_constraints_satisfaction_rate
        self.hard_constraints = ConstraintSatisfaction()
        self.soft_constraints = ConstraintSatisfaction()

        self.class_one = ClassOnePrioritySatisfaction(self.priorities)
        self.class_two = ClassTwoPrioritySatisfaction(self.priorities)

        self.free_periods: Dict[str, List[FreePeriod]] = {
            "group": [],
            "room": [],
            "instructor": []
        }
        self.clashes: Dict[str, List[Clash]] = {
            "room": [],
            "group": [],
            "instructor": []
        }
        self.capacity_inequality: List[CapacityInequality] = []

        self.maximum_consecutive_sessions: Dict[str, int] = {
            "group": int,
            "room": int,
            "instructor": int
        }

    def Evaluate(self):
 
        # Groups
        self.evaluateGroup()
        # Instructor
        self.evaluateInstructor()
        # Room
        self.evaluateRoom()

    def evaluateGroup(self):

        for group in self.group_holder:
            calculator = GroupCalculator(
                group, self.timetable.periods, self.timetable.week.days,
                self.timetable.times,
                self.timetable.configuration.consecutive["group"])
            calculator.duration_per_session = self.timetable.configuration.duration_per_session
            for session in self.timetable.sessions:
                calculator.AddSession(session)
            calculator.Calculate()
            self.clashes["group"].extend(calculator.clashes["group"])

            self.free_periods["group"].extend(calculator.free_periods)
            self.group_calculator.append(calculator)

    def evaluateInstructor(self):

        for instructor in self.instructor_holder:
            calculator = InstructorCalculator(
                instructor, self.timetable.periods, self.timetable.week.days,
                self.timetable.times,
                self.timetable.configuration.consecutive["instructor"])
            calculator.duration_per_session = self.timetable.configuration.duration_per_session
            for session in self.timetable.sessions:

                calculator.AddSession(session)
            calculator.Calculate()

            self.clashes["instructor"].extend(calculator.clashes["instructor"])

            self.free_periods["instructor"].extend(calculator.free_periods)
            self.instructor_calculator.append(calculator)

    def evaluateRoom(self):
        for room in self.room_holder:
            calculator = RoomCalculator(
                room, self.timetable.periods, self.timetable.week.days,
                self.timetable.times,
                self.timetable.configuration.consecutive["room"])
            calculator.duration_per_session = self.timetable.configuration.duration_per_session
            for session in self.timetable.sessions:
                calculator.AddSession(session)
            calculator.Calculate()
            self.clashes["room"].extend(calculator.clashes["room"])
            self.free_periods["room"].extend(calculator.free_periods)
            self.capacity_inequality.append(calculator.capacity_inequality)
            self.room_calculator.append(calculator)

    def Redefine(self):
        for old_session in self.timetable.sessions:
            new_session: Session = old_session

            # Group
            group_calculator: GroupCalculator = self.FindGroupCalculator(
                old_session.schedule.group.identifier)
            group_calculated_session: Session = group_calculator.FindSession(
                old_session.identifier)
            new_session.clash_costs[
                "group"] = group_calculated_session.clash_costs["group"]
            new_session.preference_compliance_cost[
                "group"] = group_calculated_session.preference_compliance_cost[
                    "group"]
            new_session.consecutive_cost[
                "group"] = group_calculated_session.preference_compliance_cost[
                    "group"]

            # Instructor
            instructor_calculator: InstructorCalculator = self.FindInstructorCalculator(
                old_session.schedule.instructor.identifier)
            instructor_calculated_session: Session = instructor_calculator.FindSession(
                old_session.identifier)
            new_session.clash_costs[
                "instructor"] = instructor_calculated_session.clash_costs[
                    "instructor"]
            new_session.preference_compliance_cost[
                "instructor"] = instructor_calculated_session.preference_compliance_cost[
                    "instructor"]
            new_session.consecutive_cost[
                "instructor"] = instructor_calculated_session.preference_compliance_cost[
                    "instructor"]

            # Room
            room_calculator: RoomCalculator = self.FindRoomCalculator(
                old_session.room.identifier)
            room_calculated_session: Session = room_calculator.FindSession(
                old_session.identifier)
            new_session.clash_costs[
                "room"] = room_calculated_session.clash_costs["room"]
            new_session.preference_compliance_cost[
                "room"] = room_calculated_session.preference_compliance_cost[
                    "room"]
            new_session.consecutive_cost[
                "room"] = room_calculated_session.preference_compliance_cost[
                    "room"]
            new_session.room_capacity_cost = room_calculated_session.room_capacity_cost

            # Calcualte Total Cost
            hard_constraints = ConstraintSatisfaction()
            soft_constraints = ConstraintSatisfaction()

            # Clash Costs
            hard_constraints.AddCost(new_session.clash_costs["group"],
                                     new_session.clash_costs["instructor"],
                                     new_session.clash_costs["room"])
            self.hard_constraints.AddCost(
                new_session.clash_costs["group"],
                new_session.clash_costs["instructor"],
                new_session.clash_costs["room"])

            # Room Capacity
            hard_constraints.AddCost(new_session.room_capacity_cost)

            # Prefrence and Priority Cost
            class_one = ClassOnePrioritySatisfaction(self.priorities)
            class_one.AddPreference(
                new_session.preference_compliance_cost["group"],
                new_session.preference_compliance_cost["room"],
                new_session.consecutive_cost["instructor"])
            hard_constraints.AddCost(class_one)
            self.hard_constraints.AddCost(class_one)

            class_two = ClassTwoPrioritySatisfaction(self.priorities)
            class_two.AddPreference(
                new_session.preference_compliance_cost["group"],
                new_session.preference_compliance_cost["room"],
                new_session.consecutive_cost["instructor"])
            soft_constraints.AddCost(class_two)
            self.soft_constraints.AddCost(class_two)

            # Consecutive Cost
            soft_constraints.AddCost(
                new_session.consecutive_cost["group"],
                new_session.consecutive_cost["instructor"],
                new_session.consecutive_cost["room"])
            self.soft_constraints.AddCost(
                new_session.consecutive_cost["group"],
                new_session.consecutive_cost["instructor"],
                new_session.consecutive_cost["room"])

            Total_constraints = TotalConstraintCompliance(
                hard_constraints, soft_constraints,
                self.soft_constraint_satisfaction_acceptance)

            new_session.overall_cost = Total_constraints
            new_session.hard_constraint_satisfaction = hard_constraints
            new_session.soft_constraint_satisfaction = soft_constraints

            self.timetable.ReplaceSession(old_session, new_session)

        self.Total_constraints = TotalConstraintCompliance(
            self.hard_constraints, self.soft_constraints,
            self.soft_constraint_satisfaction_acceptance)

        self.timetable.soft_constraints = self.soft_constraints
        self.timetable.hard_constraints = self.hard_constraints
        self.timetable.total_constraint = self.Total_constraints

        self.timetable.stats = {
            "rooms": {"clashes": len(self.clashes["room"]), "free": len(self.free_periods["room"])},
            "groups": {"clashes": len(self.clashes["group"]), "free": len(self.free_periods["group"])},
            "instructors": {"clashes": len(self.clashes["instructor"]), "free": len(self.free_periods["instructor"])}
          
        }

        self.timetable.free_periods = self.free_periods
        self.timetable.capacity_inequality = self.capacity_inequality

        self.timetable.clashes = self.clashes

        self.echo.print({"rooms": {"clashes": len(self.clashes["room"]), "free": len(self.free_periods["room"])},
            "groups": {"clashes": len(self.clashes["group"]), "free": len(self.free_periods["group"])},
            "instructors": {"clashes": len(self.clashes["instructor"]), "free": len(self.free_periods["instructor"])}})

    def Output(self) -> Timetable:

        return self.timetable

    def FindGroupCalculator(self, group_identifier: int) -> GroupCalculator:
        for group_calculator in self.group_calculator:
            if group_calculator.object_.identifier == group_identifier:
                return group_calculator
        sys.exit("Unable to find Group Calculator")

    def FindRoomCalculator(self, room_identifier: int) -> RoomCalculator:

        for room_calculator in self.room_calculator:
            if room_calculator.identifier == room_identifier:
                return room_calculator

    def FindInstructorCalculator(
            self, instructor_identifier: int) -> InstructorCalculator:
        for instructor_calculator in self.instructor_calculator:
            if instructor_calculator.object_.identifier == instructor_identifier:
                return instructor_calculator
