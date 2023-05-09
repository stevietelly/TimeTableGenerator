import random
from Logic.Compliance.Positive import FreePeriod
from Logic.Structure.Session import Session
from Logic.Structure.Timetable import Timetable

class Annealing:
    def __init__(self, timetable: Timetable, cooling_rate: float, heating_rate: float) -> None:
        """
        The SImulated Annealing proces has been grossly underdessigned in previous
        versions but on version 0.0.9 we chyange concepts to improve it and
        develop  Constraint Satisfaction which was more inline with what the
        algorithim did.

        We have the following
            - Cooling Rate - rated between 0.1 to 0.9, it defines the extent to
            which a timetable is allowed to cool off after heating which basically
            means an extra optimization
            - Heating Rate - rated between 0.1 to 0.9, it defines to what extent
            the timetable will be stressed to
        """
        self.cooling_rate = cooling_rate
        self.heating_rate = heating_rate