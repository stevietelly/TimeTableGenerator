class Week:
    days = []
    total_no_of_days = 0

    def __init__(self, days: list):
        self.days = days
        self.start = self.days[0]
        self.end = self.days[-1]
        self.total_no_of_days = len(self.days)

    def __str__(self):
        return f'Week:{self.start} To {self.end}'

    def __repr__(self):
        return self
