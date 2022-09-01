from Assets.DateTime.Day import Day
from Assets.DateTime.Time import Time


class DayTime:
    day_name = str
    time_string = str

    def __init__(self, day: Day, time: Time):
        self.day = day
        self.time = time
        self.format()

    def format(self):
        self.day_name = self.day.name
        self.time_string = self.time.time_string

    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.day.name} at {self.time.hour}:{self.time.minuteHandling(self.time.minute)}{self.time.state}'
