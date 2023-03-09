import sys
from typing import List, Dict, Any
from Main import Generator
from os import path
from Assets.Formation.Formats import is_valid_formart
from Assets.FileHandling.Read import Read
from Assets.DateTime.Time import is_valid_time
from Assets.DateTime.Day import DaysOfTheWeek

#  Input Files holder
input_files: Dict[str, str]= {"configurations": "Data/configuration.json", "students": "Data/students.json", "instructors": "Data/instructors.json", "rooms": "Data/rooms.json", "units": "Data/units.json", "courses": "Data/courses.json"}
output_type: str
custom_config: Dict[str, Any] = {
  "name": str,
  "days":  list,
  "start-time": str,
  "end-time": str,
  "duration-per-session": int,
  "system": {
    "limit": int,
    "saturation": bool,
    "tries": int,
    "output": str,
    "output_folder": str
  }
}

def main():
    if "-o" in sys.argv:
        o_index = sys.argv.index("-o")
        output_type = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index+1)

        
    match [len(sys.argv), True if "-c" in sys.argv else False]:
        case [1, False]:
          interface()
          generate()
        case [2, True]:
            interface(False)
            generate(False)
        case [2, False]:
            if sys.argv[1] == "defaults":
                  # send in defaults
                  generate()
        case _:
            sys.exit("Invalid inputs: Read README file for input paramaters")
          
def write_configuration_manually():
    """
    Manually write the configuration
    """
    print("Timetable Inputs")
    config_list = {"name": str, "days": int, "start-day": str, "start-time": str, "end-time": str,"duration-per-session": int}
    for config in config_list.keys():
        while True:
            input_str = input(config+": ")
            try:
                
                config_list[config] = input_str
                if type(config_list[config]) == type(input_str):
                    break
                
            except:
                print("Invalid input type")   
                sys.exit(2)

    print("Sytem Inputs Inputs")
    system_inputs = {
    "limit": int,
    "saturation": bool,
    "tries": int,
    "output": str,
    "output_folder": str
    }

    for system_input in system_inputs:
        while True:
            input_str_sys = input(system_input+": ")
            try:
                system_inputs[system_input] = input_str_sys
                break
            except:
                print("Invalid input type")   
                sys.exit(2)
    
    print("\nValidating input...........\n")
    dow = DaysOfTheWeek()
    if not dow.confirm(config_list["start-day"]):
        print("\nInvalid day -> ", config_list["start-day"])
        sys.exit(2)
    custom_config["days"] = dow.return_list_of_days(config_list["start-day"], config_list["days"])

    if not is_valid_time(config_list["start-time"]):
        print("\nInvalid Time -> ", config_list["start-time"])
        sys.exit(2)

    if not is_valid_time(config_list["end-time"]):
        print("\nInvalid Time -> ", config_list["end-time"])
        sys.exit(2)

def interface(config: bool=True):
    """
    Manually input all values one by one
    
    Config parameter
    is configuartion pre-defined?
    """
    inputs: List[str] = ["configurations", "students", "instructors", "rooms", "units", "courses"]

    print("Timetable Generator", end="\n\n")
    if not config:
        write_configuration_manually()
        inputs.pop(inputs.index("configurations"))

    
    for input_ in inputs:
        while True:
            data = input(input_.capitalize() + " file: ")
            if confirm_file(data):
                input_files[input_] =  data
                break
            print("Invalid File:")

def generate(config:bool = True, output:str="json"):
    if config:
        configurations: dict = Read(input_files["configurations"]).extract()
    else:
        configurations: dict = custom_config

    if not is_valid_formart(output):
        sys.exit("invalid output formart")

    students: dict = Read(input_files["students"]).extract()
    instructors: dict = Read(input_files["instructors"]).extract()
    rooms: dict = Read(input_files["rooms"]).extract()
    units: dict = Read(input_files["units"]).extract()
    courses: dict = Read(input_files["courses"]).extract()

    generator = Generator(configurations, students, instructors, rooms, units,courses)
    generator.initialise()
    generator.Process()
    generator.LoopCreation(max_limit=1, saturation=False, tries=1)

    timetable = generator.generate()
    timetable.Output()

def confirm_file(input_str:str):
    return  path.isfile(input_str)

if __name__ == "__main__":
    main()