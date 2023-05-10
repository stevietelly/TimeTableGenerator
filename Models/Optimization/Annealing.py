import random
from Logic.Compliance.Positive import FreePeriod
from Logic.Structure.Session import Session
from Logic.Structure.Timetable import Timetable
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.Loop.Loop import Loop
from Models.Randomizer.Randomizer import Randomizer

class Annealing:
    def __init__(self, timetable: Timetable, cooling_rate: float, temparature: float, max_iter: int) -> None:
        """
        The Simulated Annealing proces has been grossly underdessigned in previous
        versions but on version 0.0.9 we change concepts to improve it and
        develop  Constraint Satisfaction which was more inline with what the
        algorithim did.

        We have the following
            - Cooling Rate - rated between 0.1 to 0.9, it defines the extent to
            which a timetable is allowed to cool off after heating which basically
            means an extra optimization
            - Heating Index - rated between 0.1 to 0.9, it defines to what extent
            the timetable will be stressed to
        """
        self.cooling_rate = cooling_rate
        self.temparature = temparature
        self.timetable = timetable
        self.iter = max_iter

    def Process(self):
        Loop()
    
    def anneal(self):

        current_timetable = self.timetable
        FitnessEvaluation()
        for i in range(self.iter):
            Randomizer(current_timetable).Random()
        
    def anneala(self, max_iter: int) -> Timetable:
        """
        The annealing method takes the following arguments:
        - max_iter: maximum number of iterations to run the algorithm for
        """
        current_timetable = self.timetable

        for i in range(max_iter):
            # Choose a random session to move
            session_to_move = random.choice(current_timetable.sessions)

            # Choose a random time slot to move the session to
            new_time_slot = random.choice(current_timetable.time_slots)

            # Calculate the cost of the new timetable
            new_timetable = current_timetable.move_session(session_to_move, new_time_slot)
            new_cost = new_timetable.cost

            # Calculate the cost difference between the current timetable and the new timetable
            delta_cost = new_cost - current_timetable.cost

            # Decide whether to accept the new timetable or not
            if delta_cost < 0 or random.random() < self.acceptance_probability(delta_cost):
                current_timetable = new_timetable

            # Cool down the temperature
            self.temparature *= 1 - self.cooling_rate

        return current_timetable

    def acceptance_probability(self, delta_cost: float) -> float:
        """
        Calculates the probability of accepting a new solution with a higher cost
        based on the current temperature and the cost difference between the current
        solution and the new solution.
        """
        return 2.71828 ** (-delta_cost / self.temparature)
