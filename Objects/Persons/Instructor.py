class Instructor:
    name = str
    title = str
    gender = str
    identifier = str

    def __init__(self, name: str, title: str, gender: str, identifier: int):
        self.free_periods = []

        self.name = name
        self.title = title
        self.gender = gender
        self.identifier = identifier

    def __str__(self):
        return f'Instructor->{self.title}.{self.name}'

    def __repr__(self):
        return self
