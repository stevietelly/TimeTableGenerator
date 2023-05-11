"""
The process of timetable generation will involve the following process


"""
import random
import sys
from typing import Dict, List
from Assets.Functions.Echo import Echo
from Data.Parsers.Data import DataReader
from Logic.DateTime.Time import Time
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Duration import Duration
from Logic.DateTime.Week import Week
from Logic.Structure.Configuration import Configuration

from Logic.Structure.Timetable import Timetable
from Logic.Structure.Schedule import Schedule
from Logic.Structure.Session import Session
from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room


class Generator:
    # Read Data
    configuration: Configuration
    all_students: dict
    all_instructors: dict
    all_rooms: dict
    all_units: dict
    all_courses: dict

    def __init__(self, inputData: DataReader):
        
        self.configuration = inputData.configuration
        self.stats = {
            "rooms": {"clashes": 0, "free": 0},
            "groups": {"clashes": 0, "free": 0},
            "instructors": {"clashes": 0, "free": 0}
        }

        # config
        self.institution_name: str

        self.duration_per_session: int
        self.week: Week
        self.times: List[Time] = []
        self.daytimes: List[DayTime] = []

        self.schedule_holder: List[Schedule] = []
        self.session_holder: List[Session] = []

        # Holders
        self.group_holder = inputData.groups
        self.instructor_holder = inputData.instructors
        self.room_holder = inputData.rooms
        self.unit_holder: List[Unit] = inputData.units
        self.programme_holder: List[Programme] = inputData.programmes

        # Free Periods
        self.free_room_periods = []
        self.free_group_periods = []
        self.free_instructor_periods = []

        # Clashes
        self.room_clash = []
        self.group_clash = []
        self.instructor_clash = []
        self.Timeline()

        # Statistics
        self.maximum_sessions_possible: int
        self.maximum_sessions_possible_per_day: int
    
    def Timeline(self):
        current_time = self.configuration.start_time
        while self.configuration.end_time != current_time:
        
            self.times.append(current_time)
            current_time += Duration(self.configuration.duration_per_session, 0)
        self.times.append(current_time)




        days = []
        for day in self.configuration.days:
            conf_day = Day(day, self.configuration.start_time, self.configuration.end_time)
            conf_day.days = self.configuration.days
            days.append(conf_day)
            for time in self.times:
          
                self.daytimes.append(DayTime(conf_day, time))
        self.week = Week(days)
        self.configuration.week = self.week
  
    def Process(self):
        self.Scheduling()
        self.Accessioning()

        return self.generate()

    def Scheduling(self):
        """
        Create all schedules
        """
        # schedule_identifier = 1
        # unit_instructors: Dict[Unit, int] = {}
        # for course in self.programme_holder:
        #     for i, unit_holder in enumerate(course.units):
        #         year = i + 1
        #         for unit_id in unit_holder:
        #             unit: Unit = self.FindUnit(unit_id)

        #             group: Group = self.FindGroup(course.title, year)

        #             instructor_identifier: int
        #             if str(unit) in unit_instructors:
        #                 unit_instructors[str(unit)] += 1
        #             elif str(unit) not in unit_instructors:
        #                 unit_instructors[str(unit)] = 0
                    
        #             if unit_instructors[str(unit)] + 1 > len(unit.qualified_instructors):
        #                 unit_instructors[str(unit)] = 0

    
        #             instructor_identifier = unit.qualified_instructors[unit_instructors[str(unit)]]

        #             instructor: Instructor = self.FindInstructor(instructor_identifier)

        #             for _ in range(unit.sessions):
        #                 new_schedule = Schedule(schedule_identifier, unit,
        #                                         group, instructor)
        #                 self.schedule_holder.append(new_schedule)
        #             schedule_identifier += 1

        schedule_identifier = 1
        for programme in self.programme_holder:
            for i in range(programme.levels):
                year =  i + 1
                for unit_id in programme.units[i]:
                    unit: Unit = self.FindUnit(unit_id)
                    group: Group = self.FindGroup(programme.title, year)
                    instructor_identifier = random.choice(unit.qualified_instructors)
                    instructor: Instructor = self.FindInstructor(instructor_identifier)
                    for i in range(unit.sessions):
                        new_schedule = Schedule(schedule_identifier, unit, group, instructor)
                        schedule_identifier += 1
                        self.schedule_holder.append(new_schedule)
                    


    def Accessioning(self):
        """
        Sessions are schedules with a time and venue factor
        Sessions are randomized schedule-holding capsules
        """
        for i, schedule in enumerate(self.schedule_holder):
            room = random.choice(self.room_holder)
            daytime = random.choice(self.daytimes)
       
            new_session = Session(i+1, room, daytime, schedule)
          
            self.session_holder.append(new_session)

    def FindGroup(self, course_name: str, year: int) -> Group:
        """
        Find a specific Group with the course name and year
        """
      
        for group in self.group_holder:
            if group.title == course_name and group.year == year:
                return group
        sys.exit(f'unit {course_name} {year} not found')   
        
  
    def FindUnit(self, unit_identifier: int) -> Unit:
        """
        Find a specific Unit given the unit name
        """
        for unit in self.unit_holder:
            if unit.identifier == unit_identifier:
                return unit
        
        sys.exit(f'unit {unit_identifier} not found')   
       

    def FindInstructor(self, inst_id: int) -> Instructor:
        """
        Find a specific Instrcutor given the instructor id
        """
        for instructor in self.instructor_holder:
            if instructor.identifier == inst_id:
                return instructor
   
        sys.exit(f'instructor {inst_id} not found')   
        
        
    def FindSession(self, schedule_identifier: int) -> Session:
        """
        Find a specific Session given the sesssion id
        """
        session: Session 
        for session in self.session_holder:
            if session.schedule.identifier == schedule_identifier:
                return session
        sys.exit(f'session {schedule_identifier} not found')   
           
    def ReplaceSession(self, old_session: Session, new_session: Session):
        """
        This is to change a session from a previous state into a new updated one
        old session->new session
        """
        index = self.session_holder.index(old_session)
        self.session_holder[index] = new_session

    def FindRoom(self, room_name: str):
        """
        Find a specific Room given the room name
        """
        for room in self.room_holder:
            if room.name == room_name:
                return room

    def generate(self) -> Timetable:
        timetable = Timetable(self.configuration, self.daytimes, self.session_holder,self.times)
        timetable.groups = self.group_holder
        timetable.rooms = self.room_holder
        timetable.instructors = self.instructor_holder
        timetable.statistics = self.stats

        # Calculate statistics
        maximum_sessions_possible = len(self.daytimes) * len(self.room_holder)
        minimum_sessions_possible = round(len(self.daytimes) / self.configuration.total_duration_for_sessions) * len(self.room_holder)
        Echo().print({"maximum_sessions_possible": maximum_sessions_possible, "minimum_sessions_possible": minimum_sessions_possible})
        Echo().print(self.stats)
        Echo().print("Programmes: ", len(self.programme_holder), "Units: ", len(self.unit_holder), "Groups: ", len(self.group_holder), "Instructors: ", len(self.instructor_holder), "Rooms: ", len(self.room_holder))
        return timetable