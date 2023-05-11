"""
Genetic Optimization Algorithim
"""
from Assets.Functions.Echo import Echo
from Data.Parsers.Data import DataReader
from Logic.Structure.Configuration import Configuration
from Logic.Structure.Session import Session
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.Randomizer.Randomizer import Randomizer
from Logic.Structure.Timetable import Timetable
from typing import List
from Models.Generator.Generator import Generator
from Objects.User.Priorities.Priorities import Priorities

class Genetic:
    """
    Process
        - Initialization
        - fitness evaluation
        - Selection (Rank-based selection)
        - crossover
        - mutation
        - fitness evaluation
        - replacement
        - termination
    """
    def __init__(self, inputData: DataReader, parent_size: int = 2, initial_population: int = 6):
        self.initial_population = initial_population
        self.parent_selection_size = parent_size

        self.configuration: Configuration = inputData.configuration
        self.inputData = inputData
        self.instructors = inputData.instructors
        self.rooms = inputData.rooms
        self.units = inputData.units
        self.courses = inputData.programmes
        self.groups = inputData.groups
        self.priorities: Priorities = self.configuration.priorities
        self.population: List[Timetable] = []

        self.echo = Echo()

        self.echo.print(f'Running a Genetic Algorithim with {self.initial_population} initial population and a parent size of {self.parent_selection_size}')
    
    def Intialise(self):
        self.echo.print("\n")
        self.echo.print("Creating Initial Population")
        for _ in range(self.initial_population):
            generator = Generator(self.inputData)
            generator.Scheduling()
            generator.Accessioning()
            timetable = generator.generate()
            self.population.append(timetable)
            
    def Fitness(self):
        self.echo.print("\n")
        self.echo.print(f"Evaluating Fitness of {len(self.population)} Population")
        evaluated = []
        for timetable in self.population:
            fitness = FitnessEvaluation(timetable, self.inputData)
            fitness.maximum_consecutive_sessions = self.configuration.consecutive
            fitness.soft_constraint_satisfaction_acceptance = self.configuration.soft_constraints_satisfaction_rate
            fitness.Evaluate()
            fitness.Redefine()
            evaluated.append(fitness.Output())
        evaluated.sort(key=lambda t: (t.total_constraint.value))

        self.population = evaluated
    
    def Selection(self):
        self.echo.print("\n")
        self.echo.print(f"Selecting Most fit from population")
        self.echo.print(f" {len(self.population)}  Original Population")

        self.population = self.population[:int(len(self.population)/2)]
        self.echo.print(f"Reduced to {len(self.population)} Population")

    
    def Crossover(self):
        self.echo.print("\n")
        self.echo.print(f"Crossover a population of {len(self.population)}")

        timetables = []
        for i in range(0, len(self.population)):
            j = i + 1
            if not j >= len(self.population):
                parent_1 = self.population[i]
                parent_2 = self.population[j]

                child_timetable = parent_1
                child_timetable.sessions = []

                for session_1 in parent_1.sessions:
                    session_2 = parent_2.FindSession(session_1.identifier)
                    child_session = self.reproduce(session_1, session_2)
                  
                timetables.append(child_timetable)
        self.population = timetables
        self.echo.print(f"Reduced {len(self.population)} Population")

    def reproduce(self, parent_1: Session, parent_2: Session)->Session:
        new_session: Session = parent_2
        if parent_1.daytime == parent_2.daytime and parent_1.room == parent_2.room:
            return parent_1
        if parent_1.room_capacity_cost > parent_2.room_capacity_cost:
            new_session.room = parent_1.room
        return new_session

    def Mutation(self) :
        self.echo.print(f"\n")
        self.echo.print(f"Mutating {len(self.population)}")
        mutated_population: List[Session] = []
        for timetable in self.population:
            anneal = Randomizer(timetable)
            anneal.Random()
            
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

