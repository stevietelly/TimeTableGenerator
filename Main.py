"""
The entire timetable generating process comes here

# Representation
First Data structures had to be defined to represent our data and manipulate it

## External Data
Found in Objects
- Academic
    - Courses
    - Units

- Persons
    - Instructors
    - Groups of students

- Physical
    - Rooms

- User
    - Preferences
    - Priorities

## Internal Components
These are components to be used by the program, found inside Logic

- Statistics
    - Calculators
    - Costs

- Structure
    - Schedule
    - Session
    - Timetable

- FreePeriods
    - Group
    - Instructor
    - Room

- Datetime
    - Day
    - Daytime
    - Duration
    - Time
    - Week

## Models
These are functions usefull in the entire generation process
- Evaluation
- Generator
- Optimization
- Annealing


# Parsing


"""
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Data.Parsers.Data import DataReader
from Data.Validators.Type import FileTypeValidator
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time


from Models.Generator.Generator import Generator
from Models.Loop.Loop import Loop


data =  Read("Data/Defaults/data.json").extract()
reader  =  DataReader(data)
reader.Encode()



generator = Generator(reader.configuration, reader.instructors, reader.rooms, reader.units, reader.programmes, reader.groups)
raw_timetable = generator.Process()

file = Write("Output/", "data.json", raw_timetable.Output(), "json")
file.dump()


# loop = Loop(raw_timetable, reader.rooms, reader.groups, reader.instructors, reader.configuration.priorities)
# loop.Loop(max_limit=5, saturation=False)
