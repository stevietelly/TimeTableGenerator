from Objects.User.Preferences.Preference import Preferences


class Group:
    """
    A group of students means they belong to the same course and year
    """

    def __init__(self, identifier: int, title: str, year: int):
        self.identifier: int = identifier
        self.total = 0
   

        self.free_periods = []

        self.title = title
        self.year = year

     
        self.preferences: Preferences
    
    @property
    def preferences(self):
        return self._preferences
    
    @preferences.setter
    def preferences(self, value):
        self._preferences = value
    def __repr__(self):
        return self

    def __str__(self):
        return f'Group->{self.title} year {self.year}:{self.total} students'
    
    def __eq__(self, group) -> bool:
        if isinstance(group, Group):
            return False
        return (self.title == group.title) and (self.identifier == group.identifier) and (self.year == group.year)
    
    def __ne__(self, group) -> bool:
        return (self.title != group.title) or (self.identifier != group.idenifier) or (self.year != group.year)
    
     # Define the __hash__() method
    def __hash__(self):
        # Use a tuple of the instance's attributes to compute its hash value
        return hash((self.identifier, self.title, self.year))

    
    @property
    def total(self):
        return self._total
    
    @total.setter
    def total(self, value:int):
        self._total = value

