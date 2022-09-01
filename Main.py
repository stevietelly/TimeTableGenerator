import random

from Assets.DateTime.Day import Day
from Assets.DateTime.DayTime import DayTime
from Assets.DateTime.Duration import Duration
from Assets.DateTime.Time import Time
from Assets.DateTime.Week import Week
from Assets.FileHandling.Read import Read
from Logics.Calculators.Group import GroupCalculator
from Logics.Calculators.Instructor import InstructorCalculator
from Logics.Calculators.Room import RoomCalculator
from Logics.Structure.Schedule import Schedule
from Logics.Structure.Session import Session
from Objects.Academic.Courses import Course
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Student, Group
from Objects.Physical.Rooms import Room


class Generator:
    # Read Data
    configurations = None
    all_students = None
    all_instructors = None
    all_rooms = None
    all_units = None
    all_courses = None

    def __init__(self):
        # Converted Data
        # config
        self.institution_name = str
        self.start_time = Time
        self.end_time = Time
        self.duration_per_session = int
        self.week = Week
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

        self.ReadData()
        self.InitialiseData()
        self.HeaderStats()
        self.Scheduling()
        self.Accessioning()
        self.SortingStats()
        self.Accounting()
        self.Statistics()
        self.Optimizing()

        for i in range(2):
            self.ResetValues()
            self.Accounting()
            self.Statistics()

    def ReadData(self):
        # Get Configuration
        self.configurations = Read("Data/configuration.json").extract()
        self.all_students = Read("Data/students.json").extract()
        self.all_instructors = Read("Data/instructors.json").extract()
        self.all_rooms = Read("Data/rooms.json").extract()
        self.all_units = Read("Data/units.json").extract()
        self.all_courses = Read("Data/courses.json").extract()

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
            self.students_holder.append(Student(student['name'], student['course'], student['gender'], student['year']))

        del self.all_students

        """Instructors"""
        for instructor in self.all_instructors:
            self.instructor_holder.append(Instructor(instructor['name'], instructor['title'], instructor['gender'],
                                                     instructor['identifier']))

        del self.all_instructors

        """Rooms"""
        for room in self.all_rooms:
            self.room_holder.append(Room(room['identifier'], room['capacity'], room['building']))

        del self.all_rooms

        """Units"""
        for unit in self.all_units:
            self.unit_holder.append(Unit(unit['title'], unit['sessions'], unit['instructors']))
        del self.all_units

        """Courses"""
        for course in self.all_courses:
            self.course_holder.append(Course(course['course'], course['school'], course['department'], course['units']))
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
        print(f'Start Time: {self.start_time}                        Courses: total->{len(self.course_holder)}')
        print(f'End Time: {self.end_time}                         Instructors: total->{len(self.instructor_holder)}')
        print(f'{self.week}                Rooms: total->{len(self.room_holder)}')
        print(
            f'Duration Per Session: {self.duration_per_session} hour(s)                 '
            f'Units: total->{len(self.unit_holder)}')

        print(f'\nProbability: ')
        print(f'Total Sessions Per day: {len(self.times) * len(self.room_holder)}')
        print(
            f'Total Sessions per Academic week: {len(self.times) * len(self.room_holder) * self.week.total_no_of_days}')

    def SortingStats(self):
        print("\n                             Sorting, Scheduling and Accessioning")
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
                    unit = self.FindUnit(unit_name)
                    group = self.FindGroup(course.title, year)
                    if str(group) in group_instructors:
                        group_instructors[str(group)] += 1
                        if group_instructors[str(group)] > len(unit.qualified_instructors) - 1:
                            group_instructors[str(group)] = 0
                    elif str(group) not in group_instructors:
                        group_instructors[str(group)] = 0
                    instructor_identifier = unit.qualified_instructors[group_instructors[str(group)]]
                    instructor = self.FindInstructor(str(instructor_identifier))
                    for _ in range(unit.sessions):
                        new_schedule = Schedule(schedule_identifier, unit, group, instructor)
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
                original_session = self.FindSession(rc_session.schedule.identifier)
                self.ReplaceSession(original_session, rc_session)

        del room_calc, session, room

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
                original_session = self.FindSession(gc_session.schedule.identifier)
                self.ReplaceSession(original_session, gc_session)
        del group, group_calc, session, gc_session

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
                original_session = self.FindSession(ic_session.schedule.identifier)
                self.ReplaceSession(original_session, ic_session)
        del instructor, instructor_calc, session, ic_session

    def ResetValues(self):
        self.group_clash.clear()
        self.free_room_periods.clear()
        self.room_clash.clear()
        self.free_group_periods.clear()
        self.instructor_clash.clear()
        self.free_instructor_periods.clear()

    def Statistics(self):
        print("\nStats:")
        print(f'Rooms: clashes->{len(self.room_clash)} free periods->{len(self.free_room_periods)}')
        print(f'Groups: clashes->{len(self.group_clash)} free periods->{len(self.free_group_periods)}')
        print(f'Instructor: clashes->{len(self.instructor_clash)} free periods->{len(self.free_instructor_periods)}')

    def Optimizing(self):
        for clashed_room in self.room_clash:
            for index, sessions_id in enumerate(clashed_room.clashed_session_id):
                original_session = self.FindSession(sessions_id)
                if index != 0:
                    free_room_period = random.choice(self.free_room_periods)
                    mutated_session = Session(free_room_period.room, free_room_period.daytime,
                                              original_session.schedule)
                    self.ReplaceSession(original_session, mutated_session)
                    self.free_room_periods.remove(free_room_period)

        for clashed_group in self.group_clash:
            for index, sessions_id in enumerate(clashed_group.clashed_session_id):
                original_session = self.FindSession(sessions_id)
                if index != 0:
                    free_group_period = random.choice(self.FindSpecificGroupPeriod
                                                      (str(original_session.schedule.group)))
                    mutated_session = Session(original_session.room, daytime=free_group_period.daytime,
                                              schedule=original_session.schedule)
                    self.ReplaceSession(original_session, mutated_session)

        for clashed_instructor in self.instructor_clash:
            for index, sessions_id in enumerate(clashed_instructor.clashed_session_id):
                original_session = self.FindSession(sessions_id)
                if index != 0:
                    free_instructor_period = random.choice(self.FindSpecificInstructorPeriod(
                        clashed_instructor.instructor.identifier))
                    mutated_session = Session(original_session.room, free_instructor_period.daytime, original_session.schedule)
                    self.ReplaceSession(original_session, mutated_session)

    def FindGroup(self, course_name: str, year: int):
        for group in self.group_holder:
            if group.title == course_name and group.year == year:
                return group

    def FindUnit(self, unit_name: str):
        for unit in self.unit_holder:
            if unit.title == unit_name:
                return unit

    def FindInstructor(self, inst_id: str):
        for instructor in self.instructor_holder:
            if instructor.identifier == inst_id:
                return instructor

    def FindSession(self, schedule_identifier: int):
        for session in self.session_holder:
            if session.schedule.identifier == schedule_identifier:
                return session

    def ReplaceSession(self, old_session: Session, new_session: Session):
        index = self.session_holder.index(old_session)
        self.session_holder[index] = new_session

    def FindRoom(self, room_name: str):
        for room in self.room_holder:
            if room.name == room_name:
                return room

    def FindSpecificGroupPeriod(self, group_id: str):
        group_list = []
        for group_period in self.free_group_periods:
            if str(group_period.group) == group_id:
                group_list.append(group_period)
        return group_list

    def FindSpecificInstructorPeriod(self, instructor_id: int):
        instructor_list = []
        for instructor_period in self.free_instructor_periods:
            if instructor_period.instructor.identifier == instructor_id:
                instructor_list.append(instructor_period)
        return instructor_list


Generator()
