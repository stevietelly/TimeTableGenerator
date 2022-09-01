class Course:
    title = str
    school = str
    department = str
    units_per_year = str

    def __init__(self, title: str, school: str, department: str, units_per_year: list):
        self.title = title
        self.school = school
        self.department = department
        self.units_per_year = units_per_year

    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.title}'
