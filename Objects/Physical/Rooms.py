from Objects.User.Preferences.Preference import Preferences


class Room:
    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)
        return inst

    def __init__(self, identifier: int, name: str, capacity: int):
        self.name: str = name.capitalize()
        self.identifier: int = identifier
        self.capacity: int = capacity
        self.free_periods = []
    
        self.preferences: Preferences

    
    @property
    def preferences(self):
        return self._preferences
    
    @preferences.setter
    def preferences(self, value):
        self._preferences = value
        
    def __str__(self):
        return f'Room:->{self.name}'

    def __repr__(self):
        return str(self)

    def __del__(self):
        self.free_periods = []
        del self

    def __eq__(self, other):
        """
        Room Equality -> if equal
        Returns Boolean
        """
        if self.name == other.name:
            return True
        return False

    def __ne__(self, other):
        """
        Room Inequality -> if not equal
        Returns Boolean
        """
        if not self == other:
            return True
        return False
    def __hash__(self) -> int:
        return hash((self.name, self.capacity))