from Objects.User.Preferences.Preference import Preferences


class Instructor:
    def __init__(self, name: str, title: str, gender: str, identifier: int):
        self.name = name
        self.title = title
        self.gender = gender
        self.identifier: int = identifier
        self.free_periods = []
        self.preferences: Preferences

    def __eq__(self, other):
        """
        Instructor Equality -> if equal
        Returns Boolean
        """
        if isinstance(other, Instructor):
            return self.identifier == other.identifier
        return False

    def __ne__(self, other):
        """
        Instructor Inequality -> if not equal
        Returns Boolean
        """
        return not self.__eq__(other)

    def __str__(self):
        return f'Instructor: {self.title} {self.name}'

    def __repr__(self):
        return str(self)
    
    def __hash__(self) -> int:
        return hash((self.name, self.title, self.gender))
