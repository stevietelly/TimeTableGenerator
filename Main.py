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
from Assets.Functions.Echo import Echo
from Data.Parsers.Data import DataReader
from Data.Validators.Type import FileTypeValidator
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Models.Evaluation.Evaluation import FitnessEvaluation


from Models.Generator.Generator import Generator
from Models.Loop.Loop import Loop
from Models.Optimization.Constraint import ConstaraintSatisfaction
Echo.state = True


data =  Read("Data/Defaults/data.json").extract()
reader  =  DataReader(data)
reader.Encode()



generator = Generator(reader.configuration, reader.instructors, reader.rooms, reader.units, reader.programmes, reader.groups)
raw_timetable = generator.Process()

timeteable_generator = Generator(reader.configuration, reader.instructors, reader.rooms, reader.units, reader.programmes, reader.groups)
initial_timetable = timeteable_generator.Process()

evaluate = FitnessEvaluation(initial_timetable, reader.rooms, reader.groups, reader.instructors, reader.configuration.priorities)
evaluate.Evaluate()
evaluate.Redefine()
def testing(timetable):
    evaluated = FitnessEvaluation(timetable, reader.rooms, reader.groups, reader.instructors, reader.configuration.priorities)
    evaluated.Evaluate()
    evaluated.Redefine()
    timetable = evaluated.Output()

    cs = ConstaraintSatisfaction(timetable)
    cs.Optimize()
    timetable = cs.Output()
    

timetable = evaluate.Output()

# # timetable = evaluated.Output()
loop = Loop(testing, 100, timetable)
loop.Loop()
# loop = Loop(raw_timetable, reader.rooms, reader.groups, reader.instructors, reader.configuration.priorities)
# loop.Loop(max_limit=5, saturation=False)
