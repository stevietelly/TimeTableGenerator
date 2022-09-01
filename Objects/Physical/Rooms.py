class Room:
    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)
        return inst

    def __init__(self, name: str, capacity: str, building: str):
        self.name = name
        self.capacity = capacity
        self.building = building
        self.free_periods = []

    def __str__(self):
        return f'Class->{self.name} in {self.building}'

    def __repr__(self):
        return self

    def __del__(self):
        self.free_periods = []
        del self
