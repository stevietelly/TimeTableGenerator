from typing import List
from Logic.Structure.Timetable import Timetable
from Models.Evaluation.Evaluation import FitnessEvaluation
from Models.Optimization.Annealing import Annealing
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room
from Objects.User.Priorities.Priorities import Priorities


class Loop:
    def __init__(self, timetable: Timetable, rooms: List[Room], groups: List[Group], instructors: List[Instructor], priorities: Priorities) -> None:
        self.timetable = timetable
        self.rooms = rooms
        self.groups = groups
        self.instructors = instructors
        self.priorities = priorities

        self.stats = {
            "rooms": {"clashes": 0, "free": 0},
            "groups": {"clashes": 0, "free": 0},
            "instructors": {"clashes": 0, "free": 0}
        }

    def Accounting(self):
        evaluation = FitnessEvaluation(self.timetable, self.rooms, self.groups, self.instructors, self.priorities)
        evaluation.soft_constraint_satisfaction_acceptance = self.timetable.configuration.soft_constraints_satisfaction_rate
        evaluation.Evaluate()
        evaluation.Redefine()

        self.timetable = evaluation.Output()
    
    def Optimizing(self):
        annealing = Annealing(self.timetable)
        annealing.Optimize()

        self.timetable = annealing.Output()
    
    def Statistics(self, number:int=0) -> bool:
        """
        This is where clashes and free periods statistsics are calculated and printed

        I later added a return statement to allow checking if statistics are changing
        compared to the last figures, if they havent changed return False and if they have return True

        """
        print("")
        print(f'[Loop {number}: Rooms --> ', end="")
        print("{"+f'clashes: {self.timetable.stats["rooms"]["clashes"]}, free rooms periods: {self.timetable.stats["rooms"]["free"]}'+"}, Groups --> ", end="")
        print("{"+f'clashes: {self.timetable.stats["groups"]["clashes"]}, free group periods: {self.timetable.stats["groups"]["free"]}'+"}, Instructors --> ", end="")
        print("{"+f'clashes: {self.timetable.stats["instructors"]["clashes"]}, free instructor periods: {self.timetable.stats["instructors"]["free"]}'+"}]")

        stats = self.timetable.stats
        if stats == self.stats:
            self.stats = stats
            return False
        self.stats = stats
        return True

    def Loop(self, max_limit:int=1, saturation=False, tries=3):
        """
        The timetable logic is designed from here and each time, the process loops
        the data is optimized to minimise clashes as much as possible to the point of 
        saturation(where no more clashes can be optimised)

        This gives the user two options to either loop continuosly upto a maximum limit or
        upto saturation ignoring even the maximum number of times.

        Tries allows how many times we get to test for saturation, which increases
        accuracy considering that most of the allocation is random and random figures could erupt
        a number of times coincidentally, tries prevents that because three tries is just not 
        accidental anymore

        which means
        maximum limit = 0 and saturation = true -> until saturation is reached
        maximum limit > 0 and saturation = true -> loop a number of times maximum but stop if we get to saturation before
        we outdo our allowed limit
        maximum limit > 0 and saturation = False -> loop the number of times and discard even when we get to saturation

        anything beyond that should output an error
        """

        tries_count = 1
        match [True if max_limit > 0 else False, saturation]:
            case [True, True]:
                while True:
                    # Loop through a number of times
                    for i in range(max_limit):
                        self.Accounting()

                    
                        changing = self.Statistics(i+1)
                        self.Optimizing()
                      
                        if not changing and tries_count < tries:
                            tries_count += 1
                        elif not changing and tries_count == tries:
                            break   
                    break
            case [True, False]:
                # Loop through a number of times
                for i in range(max_limit):
                    self.Accounting()
                    self.Statistics(i+1)
                    self.Optimizing()
                 
            
            case [False, True]:
                tries_count = 1
                loop_count = 1
                while True:
                    loop_count += 1
                    self.Accounting()
                    changing = self.Statistics(loop_count)
                    self.Optimizing()
                    # self.ResetValues()
                    if not changing and tries_count < tries:
                        tries_count += 1
                    elif not changing and tries_count == tries:
                        break   
            case _:
                raise TypeError

