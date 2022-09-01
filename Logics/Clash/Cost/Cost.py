class Cost:
    percentage = 0

    def __init__(self, single: int, total: int):
        self.single = single
        self.total = total
        self.GetPercentage()

    def __repr__(self):
        return self

    def __str__(self):
        return f'Cost->{self.single} out of {self.total}'

    def GetPercentage(self):
        self.percentage = (self.single / self.total) * 100
