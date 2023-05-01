"""
Genetic Optimization Algorithim

Process
Initialization
fitness evaluation
Selection (Rank-based selection)
crossover
mutation
fitness evaluation
replacement
termination
"""
from Logic.Structure.Configuration import Configuration
from Logic.Structure.Session import Session
from Models.Evaluation.Evaluation import FitnessEvaluation
from Models.Optimization.Annealing import Annealing
from Objects.Persons.Students import Group
from Objects.Academic.Units import Unit
from Objects.Physical.Rooms import Room
from Objects.Persons.Instructor import Instructor
from Objects.Academic.Programme import Course
from Logic.Structure.Timetable import Timetable
from typing import List
from Models.Generator.Generator import Generator
from Objects.User.Priorities.Priorities import Priorities

class Genetic:
    def __init__(self, configuration: Configuration, instructors: List[Instructor], rooms: List[Room], units: List[Unit], courses: List[Course], groups: List[Group]):
        self.initial_population = 60
        self.parent_selection_size = 2

        self.configuration: Configuration = configuration
        self.instructors = instructors
        self.rooms = rooms
        self.units = units
        self.courses = courses
        self.groups = groups
        self.priorities: Priorities = self.configuration.priorities

        self.population: List[Timetable] = []
    
    def Intialise(self):
        for _ in range(self.initial_population):
            generator = Generator(self.configuration, self.instructors, self.rooms, self.units, self.courses, self.groups)
            generator.Scheduling()
            generator.Accessioning()
            timetable = generator.generate()
            self.population.append(timetable)
            
    def Fitness(self):
        evaluated = []
        for timetable in self.population:
            fitness = FitnessEvaluation(timetable, self.rooms, self.groups, self.instructors, self.priorities)
            fitness.maximum_consecutive_sessions = self.configuration.consecutive
            fitness.soft_constraint_satisfaction_acceptance = self.configuration.soft_constraints_satisfaction_rate
            fitness.Evaluate()
            fitness.Redefine()
            evaluated.append(fitness.Output())
        evaluated.sort(key=lambda t: (t.total_constraint.value))

        self.population = evaluated
    
    def Selection(self):
        self.population = self.population[:int(len(self.population)/2)]
    
    def Crossover(self):
        timetables = []
        for i in range(0, len(self.population)):
            j = i + 1
            if not j > len(self.population):
                parent_1 = self.population[i]
                parent_2 = self.population[j]

                child_timetable = parent_1
                child_timetable.sessions = []

                for session_1 in parent_1.sessions:
                    session_2 = parent_2.FindSession(session_1.identifier)
                    child_session = self.reproduce(session_1, session_2)
                  
                timetables.append(child_timetable)
            self.population = timetables

    def reproduce(self, parent_1: Session, parent_2: Session)->Session:
        new_session: Session = parent_2
        if parent_1.daytime == parent_2.daytime and parent_1.room == parent_2.room:
            return parent_1
        if parent_1.room_capacity_cost > parent_2.room_capacity_cost:
            new_session.room = parent_1.room
        return new_session

    def Mutation(self) :
        mutated_population: List[Session] = []
        for timetable in self.population:
            anneal = Annealing(timetable)
            anneal.Optimize()
            
            mutated_population.append(anneal.Output())
        self.population = mutated_population
            
    @property
    def initial_population(self):
        return self._initial_population

    @initial_population.setter
    def initial_population(self, value: int):
        self._initial_population = value

    @property
    def parent_selection_size(self):
        return self._parent_selection_size

    @parent_selection_size.setter
    def parent_selection_size(self, value: int):
        self._parent_selection_size = value

