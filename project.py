import sys
from typing import List, Dict, Any
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Assets.Functions.Echo import Echo
from Data.Parsers.Data import DataReader
from Data.Validators.Structure import INPUT_FILE_UNITS
from Data.Validators.Type import FileTypeValidator
from Data.Validators.Utilities import algorithm_type_validator, confirm_file_path, is_valid_day, is_valid_formart, is_valid_time, return_list_of_days
from Data.Generator.Generator import DataGenerator
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.Generator.Generator import Generator
from Models.Optimization.Genetic import Genetic


#  Input Files holder
input_files: Dict[str, str]= {"configurations": "Data/Defaults/configuration.json", "students": "Data/Defaults/students.json", "instructors": "Data/Defaults/instructors.json", "rooms": "Data/Defaults/rooms.json", "units": "Data/Defaults/units.json", "courses": "Data/Defaults/courses.json"}

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

    # for echo
    if "--echo" in sys.argv or "-e" in sys.argv:
        o_index = sys.argv.index("-e") if "-e" in sys.argv else sys.argv.index("--echo")
        state = sys.argv[o_index+1]
        if state == "on":
            Echo.state = True
        elif not state == "off":
            sys.exit("Invalid Echo status: expected values 'on' or 'off' ")
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)

    # For generating mock data for testing
    if "-dg" in sys.argv or "--data_generator" in sys.argv:
        generateData()
    
    if "run" in sys.argv:
        Run()
  
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
    
    if not is_valid_day(config_list["start-day"]):
        print("\nInvalid day -> ", config_list["start-day"])
        sys.exit(2)

    custom_config["days"] = return_list_of_days(config_list["start-day"], config_list["days"])

    if not is_valid_time(config_list["start-time"]):
        print("\nInvalid Time -> ", config_list["start-time"])
        sys.exit(2)

    if not is_valid_time(config_list["end-time"]):
        print("\nInvalid Time -> ", config_list["end-time"])
        sys.exit(2)

def Run():
    input_file: str
    output_file: str
    output_type: str

    # Define input file
    if "-i" in sys.argv or "--input_file" in sys.argv:
        o_index = sys.argv.index("-i") if "-i" in sys.argv else sys.argv.index("--input_file")
        input_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    elif "defaults" in sys.argv:
        input_file = "Data/Defaults/data.json"
    else:
        sys.exit("please Link in an input file, or run defaults")

    # Define output file
    if "-o" in sys.argv or "--output_file" in sys.argv:
        o_index = sys.argv.index("-o") if "-o" in sys.argv else sys.argv.index("--output_file")
        output_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    else:
        sys.exit("Please Define an Output file")
    
     # Output Type for the final output
    if "-tp" in sys.argv or "--output_type" in sys.argv:
        o_index = sys.argv.index("-tp") if "-tp" in sys.argv else sys.argv.index("--output_type")
        output_type = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    else:
        output_type = "json"

    Echo().print("Validating Input File.........")

    if not is_valid_formart(output_type):
        sys.exit("invalid output formart: Please Read Info for specified output formarts")
    
    data = Read(input_file).extract()
    if not FileTypeValidator(data):
        sys.exit("Invalid Input File")

    if "-a" in sys.argv or "--algorithm" in sys.argv:
        o_index = sys.argv.index("-a") if "-a" in sys.argv else sys.argv.index("--algorithm")
        algo_type = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    else:
        algo_type = "constraint_satisfaction"
    
   
        
    if not algorithm_type_validator(algo_type):
        sys.exit("Invalid Algorithm type")
    
    reader = DataReader(data)
    reader.Encode()
 

    if algo_type == "genetic":
        if "-t" in sys.argv or "--iterations" in sys.argv:
            _index = sys.argv.index("-t") if "-t" in sys.argv else sys.argv.index("--iterations")
            run_times = sys.argv[_index+1]
            try:
                int(run_times)
            except Exception as e:
                sys.exit(f"Invalid Run time \"{run_times}\"")
            sys.argv.pop(_index)
            sys.argv.pop(_index)
            RunGeneticAlgorithim(reader, run_times) 
        else:
            RunGeneticAlgorithim(reader)


    timeteable_generator = Generator(reader)
    initial_timetable = timeteable_generator.Process()

    evaluate = FitnessEvaluation(initial_timetable, reader)
    evaluate.Evaluate()


    file = Write("", output_file, evaluate.Output().Output(), output_type)
    file.dump()
    sys.exit(0)

def RunGeneticAlgorithim(inputData: DataReader, initial: int=10):
    genetic = Genetic(inputData, initial)
    genetic.Intialise()
    genetic.Fitness()
    genetic.Selection()
    genetic.Crossover()
    # genetic.Mutation()
    tt = genetic.population[0]
    print("final")
    evaluation = FitnessEvaluation(tt, inputData)
    evaluation.Evaluate()
    evaluation.Redefine()
    print(evaluation.Output().stats)
    sys.exit(1)
    
def generateData():
    print("Genarate mock data")
    input_file:str|None = None
    output_file:str|None = None

    # Define output file
    if "-o" in sys.argv or "--output_file" in sys.argv:
        o_index = sys.argv.index("-o") if "-o" in sys.argv else sys.argv.index("--output_file")
        output_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
        
    # Define input file
    if "-i" in sys.argv or "--input_file" in sys.argv:
        o_index = sys.argv.index("-i") if "-i" in sys.argv else sys.argv.index("--input_file")
        input_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    while True:
        if not output_file:
            output_file = input("Enter name of output file: ")
        print("1. Instructors\n2. Programmes, Units and Groups\n3. Rooms\n4. All Input Data")
        choice = input("Pick one of the above: ")

        generator = DataGenerator(output_file)
        inputs = Read(input_file).extract()
        match choice:
            case '1':
                total = int(input("How many instructors would you like? ")) if not input_file else int(inputs['instructors'])
                generator.GenerateInstructors(total)
                generator.write()
                sys.exit(3)
            case '2':
                prog = int(input("How many Programmes would you like? ")) if not input_file else int(inputs["programmes"])
                inst = int(input("How many instructors do you have? ")) if not input_file else int(inputs["instructors"])
                generator.GenerateProgrammesUnitsGroups(prog, inst)
                generator.write()
                sys.exit()
            case '3':
                total = int(input("How many rooms would you like?: ")) if not input_file else int(inputs["rooms"])
                generator.GenerateRooms(total)
                generator.write()
                sys.exit()
            case '4':
                instructors = input("How many instructors would you like? ") if not input_file else int(inputs["instructors"])
                rooms = input("How many rooms would you like? ") if not input_file else int(inputs["rooms"])
                programmes = input("How many programmes would you like? ") if not input_file else int(inputs["programmes"])
                if "-c" in sys.argv or "--configuration" in sys.argv:
                    o_index = sys.argv.index("-c") if "-c" in sys.argv else sys.argv.index("--configuration")
                    config = Read(sys.argv[o_index+1]).extract()
                    sys.argv.pop(o_index)
                    sys.argv.pop(o_index)
                    generator.GenerateAllInputData(instructors, programmes, rooms, config)
                    generator.write()
                else:
                    write_configuration_manually()        
                    generator.GenerateAllInputData(instructors, programmes, rooms, custom_config)
                    generator.write()
                sys.exit()



if __name__ == "__main__":
    main()