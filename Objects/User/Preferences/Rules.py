from typing import Union
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime

from Logic.DateTime.Time import Time

class Rule:
    def __init__(self, value: Union["Rule", list, Day, DayTime, Time]) -> None:
        self.value = value
        self.quality =  None
       

class Before(Rule):
    def __init__(self, value: Union[Time, Day, DayTime]) -> None:
        super().__init__(value)
        """This defines the before or less than <"""
        self.quality = "before"

    def __str__(self):
        return f"Before {str(self.value)}"

    def __repr__(self):
        return f"Before({repr(self.value)})"

class After(Rule):
    def __init__(self, value: Union[Time, Day, DayTime]) -> None:
        super().__init__(value)
        """This defines the after or greater than >"""
        self.quality = " after"
    
    def __str__(self):
        return f"After {str(self.value)}"

    def __repr__(self):
        return f"After({repr(self.value)})"

class Except(Rule):
    def __init__(self, value: list) -> None:
        super().__init__(value)
        """This defines all values except"""
        self.quality = "except"

    def __str__(self):
        return f"Except {str(self.value)}"

    def __repr__(self):
        return f"Except({repr(self.value)})"

class All(Rule):
    def __init__(self) -> None:
        super().__init__(None)
        """This defines all values"""
        self.quality = "all"

    def __str__(self):
        return "All"

    def __repr__(self):
        return "All()"

class Only(Rule):
    def __init__(self, value:list) -> None:
        super().__init__(value)
        """This defines specific values"""
        self.quality = "only"

    def __str__(self):
        return f"Only {str(self.value)}"

    def __repr__(self):
        return f"Only({repr(self.value)})"


class Conjuction(Rule):
    def __init__(self, primary:Rule, secondary: Rule) -> None:
        super().__init__(None)
        self.quality = None
        self.primary = primary
        self.secondary = secondary

class And(Conjuction):
    def __init__(self, primary: Rule, secondary: Rule) -> None:
        super().__init__(primary, secondary)
        """This defines the additon conjuction"""
        self.quality = "and"
    
    def __str__(self):
        return f"{str(self.primary)} and {str(self.secondary)}"

    def __repr__(self):
        return f"And({repr(self.primary)}, {repr(self.secondary)})"

class Or(Conjuction):
    def __init__(self, primary: Rule, secondary: Rule) -> None:
        super().__init__(primary, secondary)
        """This define the opposite of and"""
        self.quality = "or"
    
    def __str__(self):
        return f"{str(self.primary)} or {str(self.secondary)}"

    def __repr__(self):
        return f"Or({repr(self.primary)}, {repr(self.secondary)})"
