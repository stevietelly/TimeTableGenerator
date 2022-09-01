class Duration:
    hour = 0
    minute = 0

    def __init__(self, hour: int, minute: int):
        self.hour = hour
        self.minute = minute

    def __repr__(self):
        return self

    def __str__(self):
        if self.minute == 0:
            return f'{self.hour}hour(s)'
        elif self.minute != 0:
            return f'{self.hour}hour(s) and {self.minute} minute(s)'
