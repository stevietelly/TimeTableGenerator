from Assets.DateTime.Time import Time


class Day:
    start_time = Time
    end_time = Time

    def __init__(self, name, start: Time, end: Time):
        self.name = name
        self.start_time = start
        self.end_time = end

    def __repr__(self):
        return self

    def __str__(self):
        return f'Day->{self.name}'
