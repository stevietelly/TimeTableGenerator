from typing import List
from Logic.DateTime.Time import Time



class Day:
    week = None
    days: List[str]
    # TODO: Do not forget to insert this value
    def __init__(self, name: str, start: Time, end: Time):
        self.name = name
        self.start_time: Time = start
        self.end_time: Time = end
    
    def __add__(self, other: int):
        if isinstance(other, int):
            new_index = (self.days.index(self.name) + other) % len(self.days)
            return Day(self.days[new_index], self.start_time, self.end_time)
        raise TypeError("unsupported operand type(s) for +: 'Day' and '{}'".format(type(other).__name__))
    
    def __sub__(self, other: int):
        if isinstance(other, int):
            new_index = (self.days.index(self.name) - other) % len(self.days)
            return Day(self.days[new_index], self.start_time, self.end_time)
        raise TypeError("unsupported operand type(s) for +: 'Day' and '{}'".format(type(other).__name__))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Day:->{self.name}'
    
    def __eq__(self, other):
        if isinstance(other, Day):
            return self.name == other.name
        return False
    
    def __ne__(self, other):
        if isinstance(other, Day):
            return self.name != other.name
        return True

    
    def __lt__(self, other):
        if isinstance(other, Day):
            return self.days.index(self.name) < self.days.index(other.name)
        return False
    
    def __le__(self, other):
        if isinstance(other, Day):
            return self.days.index(self.name) <= self.days.index(other.name)
        return False
    
    def __gt__(self, other):
        if isinstance(other, Day):
            return self.days.index(self.name) > self.days.index(other.name)
        return False
    
    def __ge__(self, other):
        if isinstance(other, Day):
            return self.days.index(self.name) >= self.days.index(other.name)
        return False

    
    @staticmethod
    def generate_days(start_day: str, num_days: int) -> List[str]:
        days_in_week: List[str] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        start_day_index: int = days_in_week.index(start_day.lower())
        days: List[str] = []
        for i in range(num_days):
            days.append(days_in_week[(start_day_index + i) % 7])
        return days