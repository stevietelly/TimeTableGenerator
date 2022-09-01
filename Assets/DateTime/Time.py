from Assets.DateTime.Duration import Duration


class Time:
    time_string = str

    hour = 0  # 0 to 23
    minute = 0  # 0 to 59
    state = None  # am or pm

    def __init__(self, time_string: str):
        self.time_string = time_string
        self.format()
        self.clockSystemHandling()

    def format(self):
        temp = None

        hour_mode = True
        minute_mode = False
        state_mode = False
        for element in self.time_string:
            if element == ":" and hour_mode:
                self.hour = int(temp)
                temp = None
                hour_mode = False
                minute_mode = True
            elif hour_mode:
                if temp is None:
                    temp = element
                elif temp is not None:
                    temp += element
            elif element in "amp" and minute_mode:
                self.minute = int(temp)
                minute_mode = False
                state_mode = True
                temp = element
            elif minute_mode:
                if temp is None:
                    temp = element
                elif temp is not None:
                    temp += element
            elif state_mode:
                temp += element

        self.state = temp

    def clockSystemHandling(self):
        if self.state == "pm" and self.hour < 12:
            self.hour += 12

    @staticmethod
    def minuteHandling(minute: int):
        if minute < 10:
            return f'0{minute}'
        return minute

    def __repr__(self):
        return self

    def __str__(self):
        return f'Time->{self.hour}:{self.minuteHandling(self.minute)}{self.state}'

    def __add__(self, other):
        """Returns Time"""
        hour = self.hour + other.hour
        minute = self.minute + other.minute

        time = Time("0:00am")
        time.hour = hour
        time.minute = minute

        if hour > 11:
            time.state = "pm"

        return time

    def __eq__(self, other):
        if self.hour == other.hour and self.minute == other.minute:
            return True
        return False

    def __sub__(self, other):
        """
        Returns Duration
        """
        hour = self.hour - other.hour
        minute = self.minute - other.minute
        duration = Duration(hour, minute)
        return duration


