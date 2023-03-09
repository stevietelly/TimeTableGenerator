from os import path
from datetime import datetime


def confirm_file_path(input_str:str)->bool:
    return  path.isfile(input_str)

def is_valid_time(time_str)->bool:
    try:
        if len(time_str) == 5:
            datetime.strptime(time_str, '%H:%M')
        elif len(time_str) == 8:
            datetime.strptime(time_str, '%I:%M:%S %p')
        else:
            return False
        return True
    except ValueError:
        return False

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
def is_valid_day(self, day:str)->bool:
    if day.lower() in self.days:
        return True
    return False

def return_list_of_days(self, start_day:str, no_of_days:int) -> list | None:
    no_of_days_mod = no_of_days -1
    if no_of_days_mod > 6:
        return None
    index_of_day = self.days.index(start_day)
    return self.days[index_of_day:no_of_days_mod]