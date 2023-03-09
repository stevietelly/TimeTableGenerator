import random

from Assets.DateTime.Day import Day
from Assets.DateTime.DayTime import DayTime
from Assets.DateTime.Duration import Duration
from Assets.DateTime.Time import Time
from Assets.DateTime.Week import Week
from Assets.FileHandling.Format import Format
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Logics.Calculators.Group import GroupCalculator
from Logics.Calculators.Instructor import InstructorCalculator
from Logics.Calculators.Room import RoomCalculator
from Logics.Structure.Schedule import Schedule
from Logics.Structure.Session import Session, NullSession
from Logics.Structure.Timetable import Timetable
from Objects.Academic.Courses import Course
from Objects.Academic.Units import NullUnit, Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Student, Group, NullGroup
from Objects.Physical.Rooms import Room


class Generator:
    # Read Data
    configurations: dict
    all_students: dict
    all_instructors: dict
    all_rooms: dict
    all_units: dict
    all_courses: dict

    def __init__(self, configuration: dict, students: dict, instructors: dict, rooms: dict, units: dict,
                 courses: dict):
        
        self.configurations: dict = configuration
        self.all_students: dict = students
        self.all_instructors: dict = instructors
        self.all_rooms: dict = rooms
        self.all_units: dict = units
        self.all_courses: dict = courses

        self.stats = {
            "rooms": {"clashes": 0, "free": 0},
            "groups": {"clashes": 0, "free": 0},
            "instructors": {"clashes": 0, "free": 0}
        }

        # config
        self.institution_name: str
        self.start_time: Time
        self.end_time: Time
        self.duration_per_session: int
        self.week: Week
        self.times = []
        self.daytimes = []

        self.group_holder = []
        self.schedule_holder = []
        self.session_holder = []

        # Holders
        self.students_holder = []
        self.instructor_holder = []
        self.room_holder = []
        self.unit_holder = []
        self.course_holder = []

        # Free Periods
        self.free_room_periods = []
        self.free_group_periods = []
        self.free_instructor_periods = []

        # Clashes
        self.room_clash = []
        self.group_clash = []
        self.instructor_clash = []



    def initialise(self):
   
        self.InitialiseData()
        self.HeaderStats()

    def Process(self):
        self.Scheduling()
        self.Accessioning()
        self.SortingStats()
    
    def LoopCreation(self, max_limit:int=1, saturation=False, tries=3):
        """
        The timetable logic is designed from here and each time, the process loops
        the data is optimized to minimise clashes as much as possible to the point of 
        saturation(where no more clashes can be optimised)

        This gives the user two options to either loop continuosly upto a maximum limit or
        upto saturation ignoring even the maximum number of times.

        Tries allows how many times we get to test for saturation, which increases
        accuracy considering that most of the allocation is random and random figures could erupt
        a number of times coincidentally, tries prevents that because three tries is just not 
        accidental anymore

        which means
        maximum limit = 0 and saturation = true -> until saturation is reached
        maximum limit > 0 and saturation = true -> loop a number of times maximum but stop if we get to saturation before
        we outdo our allowed limit
        maximum limit > 0 and saturation = False -> loop the number of times and discard even when we get to saturation

        anything beyond that should output an error
        """
    
        tries_count = 1
        match [True if max_limit > 0 else False, saturation]:
            case [True, True]:
                while True:
                    # Loop through a number of times
                    for i in range(max_limit):
                        self.Accounting()
                        changing = self.Statistics(i+1)
                        self.Optimizing()
                        self.ResetValues()
                        if not changing and tries_count < tries:
                            tries_count += 1
                        elif not changing and tries_count == tries:
                            break   
                    break
            case [True, False]:
                # Loop through a number of times
                for i in range(max_limit):
                    self.Accounting()
                    self.Statistics(i+1)
                    self.Optimizing()
                    self.ResetValues()
            
            case [False, True]:
                tries_count = 1
                loop_count = 1
                while True:
                    loop_count += 1
                    self.Accounting()
                    changing = self.Statistics(loop_count)
                    self.Optimizing()
                    self.ResetValues()
                    if not changing and tries_count < tries:
                        tries_count += 1
                    elif not changing and tries_count == tries:
                        break   
            case _:
                raise TypeError


    def InitialiseData(self):
        """Configurations"""
        self.institution_name = self.configurations['name']
        self.start_time = Time(self.configurations['start-time'])
        self.end_time = Time(self.configurations['end-time'])
        self.duration_per_session = self.configurations['duration-per-session']

        """Handle Timeline"""
        # create daytimes

        current_time = self.start_time
        while self.end_time != current_time:
            self.times.append(current_time)
            current_time += Duration(self.duration_per_session, 0)
        self.times.append(current_time)

        days = []
        for day in self.configurations['days']:
            conf_day = Day(day, self.start_time, self.end_time)
            days.append(conf_day)
            for time in self.times:
                self.daytimes.append(DayTime(conf_day, time))
            del conf_day

        self.week = Week(days)
        del days
        del self.configurations

        """Students"""
        for student in self.all_students:
            self.students_holder.append(
                Student(student['name'], student['course'], student['gender'],
                        student['year']))

        del self.all_students

        """Instructors"""
        for instructor in self.all_instructors:
            self.instructor_holder.append(
                Instructor(instructor['name'], instructor['title'],
                           instructor['gender'], instructor['identifier']))

        del self.all_instructors

        """Rooms"""
        for room in self.all_rooms:
            self.room_holder.append(
                Room(room['identifier'], room['capacity'], room['building']))

        del self.all_rooms

        """Units"""
        for unit in self.all_units:
            self.unit_holder.append(
                Unit(unit['title'], unit['sessions'], unit['instructors']))
        del self.all_units

        """Courses"""
        for course in self.all_courses:
            self.course_holder.append(
                Course(course['course'], course['school'],
                       course['department'], course['units']))
            for i in range(len(course["units"])):
                self.group_holder.append(Group(course['course'], i + 1))
        del self.all_courses

        """Place all the students into their respective groups"""
        for student in self.students_holder:

            self.FindGroup(student.course, student.year).AddStudent(student)

    def HeaderStats(self):
        print(f'                                      {self.institution_name}')
        print(
            f"                                                Students: total->{len(self.students_holder)}  divided "
            f"into groups->{len(self.group_holder)}")
        print(
            f'Start Time: {self.start_time}                        Courses: total->{len(self.course_holder)}'
        )
        print(
            f'End Time: {self.end_time}                         Instructors: total->{len(self.instructor_holder)}'
        )
        print(
            f'{self.week}                Rooms: total->{len(self.room_holder)}'
        )
        print(
            f'Duration Per Session: {self.duration_per_session} hour(s)                 '
            f'Units: total->{len(self.unit_holder)}')

        print(f'\nProbability: ')

        print(
            f'Total Sessions Per day: {len(self.times) * len(self.room_holder)}'
        )
        print(
            f'Total Sessions per Academic week: {len(self.times) * len(self.room_holder) * self.week.total_no_of_days}'
        )

    def SortingStats(self):
        print(
            "\n                             Sorting, Scheduling and Accessioning"
        )
        print(f'Schedules: Created total->{len(self.schedule_holder)}')
        if len(self.schedule_holder) == len(self.session_holder):
            session_info = f'All schedules allocated a room and time of day'
        else:
            difference = len(self.schedule_holder) - len(self.session_holder)
            session_info = f'{len(self.schedule_holder) - difference}' \
                           f' schedules allocated a room and time of day except {difference}'
        print(f'Sessions: {session_info}')

    def Scheduling(self):
        schedule_identifier = 1
        group_instructors = {}
        for course in self.course_holder:
            for i, unit_holder in enumerate(course.units_per_year):
                year = i + 1
                for unit_name in unit_holder:

                    unit: Unit = self.FindUnit(unit_name)

                    group: Group = self.FindGroup(course.title, year)
                    if str(group) in group_instructors:
                        group_instructors[str(group)] += 1
                        # type: ignore 
                        if group_instructors[str(group)] > len(
                                unit.qualified_instructors) - 1:
                                                       
                            group_instructors[str(group)] = 0
                    elif str(group) not in group_instructors:
                        group_instructors[str(group)] = 0
                    instructor_identifier = unit.qualified_instructors[
                        group_instructors[str(group)]]
                    instructor = self.FindInstructor(
                        str(instructor_identifier))
                    for _ in range(unit.sessions):
                        new_schedule = Schedule(schedule_identifier, unit,
                                                group, instructor)
                        self.schedule_holder.append(new_schedule)
                        schedule_identifier += 1

    def Accessioning(self):
        """
        Sessions are schedules with a time and venue factor
        Sessions are randomized schedule-holding capsules
        """
        for schedule in self.schedule_holder:
            room = random.choice(self.room_holder)
            daytime = random.choice(self.daytimes)
            new_session = Session(room, daytime, schedule)
            self.session_holder.append(new_session)

    def Accounting(self):
        """Rooms"""
        for room in self.room_holder:
            room_calc = RoomCalculator(room, self.daytimes)
            for session in self.session_holder:
                if room_calc.identifier == session.room.name:
                    room_calc.AddSession(session)
            room_calc.Populate()
            room.free_periods = room_calc.free_periods
            self.free_room_periods.extend(room_calc.free_periods)
            self.room_clash.extend(room_calc.room_clashes)

            for rc_session in room_calc.clashed:
                original_session = self.FindSession(
                    rc_session.schedule.identifier)
                self.ReplaceSession(original_session, rc_session)
        
        """Group"""
        for group in self.group_holder:
            group_calc = GroupCalculator(group, self.daytimes)
            for session in self.session_holder:
                if group_calc.identifier == str(session.schedule.group):
                    group_calc.AddSession(session)
            group_calc.Populate()
            self.free_group_periods.extend(group_calc.free_periods)
            group.free_periods.extend(group_calc.free_periods)
            self.group_clash.extend(group_calc.group_clashes)

            for gc_session in group_calc.clashed:
                original_session = self.FindSession(
                    gc_session.schedule.identifier)
                self.ReplaceSession(original_session, gc_session)

        """Instructor"""
        for instructor in self.instructor_holder:
            instructor_calc = InstructorCalculator(instructor, self.daytimes)
            for session in self.session_holder:
                if instructor_calc.identifier == session.schedule.instructor.identifier:
                    instructor_calc.AddSession(session)
            instructor_calc.Populate()
            self.free_instructor_periods.extend(instructor_calc.free_periods)
            instructor.free_periods.extend(instructor_calc.free_periods)
            self.instructor_clash.extend(instructor_calc.instructor_clashes)

            for ic_session in instructor_calc.clashed:
                original_session = self.FindSession(
                    ic_session.schedule.identifier)
                self.ReplaceSession(original_session, ic_session)

    def ResetValues(self):
        self.group_clash.clear()
        self.free_room_periods.clear()
        self.room_clash.clear()
        self.free_group_periods.clear()
        self.instructor_clash.clear()
        self.free_instructor_periods.clear()

    def Statistics(self, number:int=0) -> bool:
        """
        This is where clashes and free periods statistsics are calculated and printed

        I later added a return statement to allow checking if statistics are changing
        compared to the last figures, if they havent changed return False and if they have return True

        """
        print("")
        print(f'[Loop {number}: Rooms --> ', end="")
        print("{"+f'clashes: {len(self.room_clash)}, free rooms periods: {len(self.free_room_periods)}'+"}, Groups --> ", end="")
        print("{"+f'clashes: {len(self.group_clash)}, free group periods: {len(self.free_group_periods)}'+"}, Instructors --> ", end="")
        print("{"+f'clashes: {len(self.instructor_clash)}, free instructor periods: {len(self.free_instructor_periods)}'+"}]")

        stats = {
            "rooms": {"clashes": len(self.room_clash), "free": len(self.free_room_periods)},
            "groups": {"clashes": len(self.group_clash), "free": len(self.free_group_periods)},
            "instructors": {"clashes": len(self.instructor_clash), "free": len(self.free_instructor_periods)}
        }
        if stats == self.stats:
            self.stats = stats
            return False
        self.stats = stats
        return True

    def Optimizing(self):
        """
        This function takes all clashing objects and tries to solve them (optimizing all clashes)
        """
        for clashed_room in self.room_clash:
            for index, sessions_id in enumerate(
                    clashed_room.clashed_session_id):
                original_session: Session = self.FindSession(sessions_id)
                if index != 0:
                    free_room_period = random.choice(self.free_room_periods)
                    mutated_session = Session(free_room_period.room,
                                              free_room_period.daytime,
                                              original_session.schedule)
                    self.ReplaceSession(original_session, mutated_session)
                    self.free_room_periods.remove(free_room_period)

        for clashed_group in self.group_clash:
            for index, sessions_id in enumerate(
                    clashed_group.clashed_session_id):
                original_session: Session = self.FindSession(sessions_id)
                if index != 0:
                    free_group_period = random.choice(
                        self.FindSpecificGroupPeriod(
                            str(original_session.schedule.group)))
                    mutated_session = Session(
                        original_session.room,
                        daytime=free_group_period.daytime,
                        schedule=original_session.schedule)
                    self.ReplaceSession(original_session, mutated_session)

        for clashed_instructor in self.instructor_clash:
            for index, sessions_id in enumerate(
                    clashed_instructor.clashed_session_id):
                original_session = self.FindSession(sessions_id)
                if index != 0:
                    free_instructor_periods = self.FindSpecificInstructorPeriod(
                            clashed_instructor.instructor.identifier)
                    if  len(free_instructor_periods) > 0:
                        free_instructor_period = random.choice(free_instructor_periods)
                        mutated_session = Session(original_session.room,
                                                free_instructor_period.daytime,
                                                original_session.schedule)
                        self.ReplaceSession(original_session, mutated_session)

    def FindGroup(self, course_name: str, year: int) -> Group:
        """
        Find a specific Group with the course name and year
        """
      
        for group in self.group_holder:
            if group.title == course_name and group.year == year:
                return group
        return NullGroup()

    def FindUnit(self, unit_name: str) -> Unit:
        """
        Find a specific Unit given the unit name
        """
        for unit in self.unit_holder:
            if unit.title == unit_name:
                return unit
        return NullUnit()

    def FindInstructor(self, inst_id: str):
        """
        Find a specific Instrcutor given the instructor id
        """
        for instructor in self.instructor_holder:
            if instructor.identifier == inst_id:
                return instructor

    def FindSession(self, schedule_identifier: int) -> Session:
        """
        Find a specific Session given the sesssion id
        """
        session: Session 
        for session in self.session_holder:
            if session.schedule.identifier == schedule_identifier:
                return session
        return NullSession()      

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
    
    def FindSpecificGroupPeriod(self, group_id: str) -> list:
        """
        This function finds a list of Free group periods( a time in which a specific group is free) given 
        the group id
        """
        group_list = []
        for group_period in self.free_group_periods:
            if str(group_period.group) == group_id:
                group_list.append(group_period)
        return group_list

    def FindSpecificInstructorPeriod(self, instructor_id: int) -> list:
        """
        This function finds a list of Free instructor periods( a time in which a specific instructor is free) given 
        the instructor id
        """
        instructor_list = []
        for instructor_period in self.free_instructor_periods:
            if instructor_period.instructor.identifier == instructor_id:
                instructor_list.append(instructor_period)
        return instructor_list

    def generate(self) -> Timetable:
        timetable = Timetable(self.week, self.times, self.session_holder)
        timetable.groups = self.group_holder
        timetable.rooms = self.room_holder
        timetable.students = self.students_holder
        timetable.instructors = self.instructor_holder
        timetable.statistics = self.stats
        timetable.title =  self.institution_name
        return timetable
