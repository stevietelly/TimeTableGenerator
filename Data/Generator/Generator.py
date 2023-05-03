import random
import string

from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write


class DataGenerator:
    people = Read("Data\Generator\people.json").extract()
    programmes = Read("Data\Generator\programmes.json").extract()
    units = Read("Data\Generator\modules.json").extract()

    def __init__(self, output_file:str):
        """
        A class to generate random data for the sake of testing
        """
        self.output_file = output_file
        self.output = {}
    
    def generateRandomPrefrence(self, objects: list|None = None):
        return None

    def GenerateInstructors(self, total:int):
        temp = random.sample(self.people, int(total))

        result = []
        for index, datum in enumerate(temp):
            result.append({'name': datum['first_name'] + " " + datum['last_name'], 'title': datum['title'], 'gender': datum['gender'], 'identifier': index + 1})
        
        self.output["instructors"] = result
    
    def GenerateRooms(self, total):
        total = int(total)
        result = []
        for i in range(total):
            name = ''.join(random.choices(string.ascii_uppercase, k=5))
            capacity = random.randint(20, 100)
            
            temp = {
                "identifier": i + 1,
                "name": name,
                "capacity": capacity,
                "preferences": self.generateRandomPrefrence()
            }
            result.append(temp)
        self.output["rooms"] = result
            
    def _HandleProgrammes(self, total: int, instructors: int):
        total = int(total)
        programmes = random.sample(self.programmes, total)

        result = []
        for index, p in enumerate(programmes):
            levels =  random.randint(1, 4)
            units = self._GenerateUnits(total * 9, instructors, levels)

            temp = {"identifier": index + 1, "title": p, "levels": levels, "units": self.UnitHandling(levels, len(units))}
            result.append(temp)
        
        return result, units

    def GenerateProgrammesUnitsGroups(self, total:int, inst:int):
        programmes, units = self._HandleProgrammes(total, inst)
        
        self.output["programmes"] = programmes
        self.output["units"] = units
        self.output["groups"] = self.GroupHandling(programmes)
    
    def GroupHandling(self, programmes: list):
        count = 1
        result = []
        for program in programmes:
            

            for level in range(program["levels"]):
              
                temp = {"identifier": count, "programme": program["title"], "year": level + 1, "total": random.randint(20, 100)}
                result.append(temp)
                count += 1
        return result

    def UnitHandling(self, levels:int, total_units: int):
        units =  random.randint(3, 9)
        result = []
        for _ in range(levels):
            temp = []
            for _ in range(units):
                unit = random.randint(1, total_units)
                temp.append(unit)
            result.append(temp)
        return result

    def _GenerateUnits(self, total: int, no_of_instructors: int, levels:int):
        units = random.sample(self.units, total)
        result = []
        for i, unit in enumerate(units):
            temp = {"identifier": i + 1,"title": unit, "prefrences": self.generateRandomPrefrence(), "instructors": self._UnitInstructorHandling(no_of_instructors), "sessions": random.randrange(1, 3)}
            result.append(temp)
        return result
    
    def _UnitInstructorHandling(self, total_instructors: int):
        result = []
     
        n = random.randint(2, 9)
        temp = []
        for _ in range(n):
            c = random.randint(1, int(total_instructors))
            temp.append(c) if not c in temp else None
     
        return temp

    def GenerateAllInputData(self, instructors:int, programmes:int, rooms:int, configuration):
        
        self.output["configuration"] =  configuration["configuration"]
        self.GenerateInstructors(instructors)
        self.GenerateRooms(rooms)
        self.GenerateProgrammesUnitsGroups(programmes, instructors)

    def write(self):
        w = Write('', self.output_file, self.output)
        w.dump()


