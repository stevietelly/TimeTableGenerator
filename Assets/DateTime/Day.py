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

class DaysOfTheWeek:
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    def confirm(self, day:str):
        if day.lower() in self.days:
            return True
        return False
    def return_list_of_days(self, start_day:str, no_of_days:int):
       no_of_days_mod = no_of_days -1
       if no_of_days_mod > 6:
           return None
       index_of_day = self.days.index(start_day)
       return self.days[index_of_day:no_of_days_mod]