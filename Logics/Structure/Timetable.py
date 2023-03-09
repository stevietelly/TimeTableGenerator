from Assets.DateTime.Week import Week
from Assets.FileHandling.Format import Format
from Assets.FileHandling.Write import Write


class Timetable:
    def __init__(self, week: Week, periods: list, sessions: list):
        self.week = week
        self.periods = periods
        self.sessions = sessions
    
    def Output(self, file_path:str):
        format_ = Format(self.sessions)
        result = format_.GiveResult()

        writer = Write("Bin/html/", "main.json", result)
        writer.dump()
    
    @property 
    def week(self):
        return self._week
        
    @week.setter
    def week(self, value):
        self._week = value

    @property 
    def sessions(self):
        return self._sessions
        
    @sessions.setter
    def sessions(self, value):
        self._sessions = value

    @property 
    def periods(self):
        return self._periods
        
    @periods.setter
    def periods(self, value):
        self._periods = value

    @property 
    def rooms(self):
        return self._rooms
        
    @rooms.setter
    def rooms(self, value):
        self._rooms = value
    
    @property 
    def students(self):
        return self._students
        
    @students.setter
    def students(self, value):
        self._students = value
    
    @property 
    def instructors(self):
        return self._instructors
        
    @instructors.setter
    def instructors(self, value):
        self._instructors = value

    @property 
    def groups(self):
        return self._groups
        
    @groups.setter
    def groups(self, value):
        self._groups = value

    @property 
    def statistics(self):
        return self._statistics
        
    @statistics.setter
    def statistics(self, value: dict):
        self._statistics = value

    @property 
    def title(self):
        return self._statistics
        
    @title.setter
    def title(self, value: str):
        self._statistics = value