from typing import List


class Programme:
    title = str
    school = str
    department = str
 

    def __init__(self, identifier: int,  title: str, levels: int):
        self.title = title
        self.identifier = identifier
        self.levels = levels
        self.units: List[List[int]]


    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.title}'
