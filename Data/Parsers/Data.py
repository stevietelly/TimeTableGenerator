from typing import List
from Assets.FileHandling.Read import Read

from Objects.Physical.Rooms import Room
from Objects.User.Preferences.Preference import Preferences
from Objects.User.Preferences.Rules import  All

from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit
from Logic.Structure.Configuration import Configuration
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.User.Priorities.Priorities import Priorities



class DataReader:
    def __init__(self, data):
        """
        DataReader Takes in the input file and converts
        everything into python objects to be used by the program.
        It essentially Encodes everything into the right python 
        Object
        """
        self.configuration: Configuration
        self.programmes: List[Programme] = []
        self.units: List[Unit] = []
        self.instructors: List[Instructor] = []
        self.groups: List[Group] = []
        self.rooms: List[Group] = []

        self.data = data
    
    def Encode(self) -> None:
        self._create_configurations(self.data["configuration"])
        self._create_rooms(self.data["rooms"])
        self._create_programmes(self.data.get('programmes', []))
        self._create_units(self.data.get('units', []))
        self._create_instructors(self.data.get('instructors', []))
        self._create_groups(self.data.get('groups', []))
    
    def _create_programmes(self, data: List[dict]) -> None:
        for program_data in data:
            id_ = program_data["identifier"]
            title = program_data['title']
            levels = program_data['levels']
            units = program_data["units"]
            
            programme = Programme(id_, title, levels)
            programme.units = units
            self.programmes.append(programme)
    
    def _create_units(self, data: List[dict]) -> None:
        for unit_data in data:
            id_ = unit_data['identifier']
            qualified = unit_data['instructors']
            title = unit_data['title']
            sessions = unit_data['sessions']
            preferences = self._create_preferences(unit_data.get('preferences', []))
            
            unit = Unit(id_, title, sessions, qualified)
            unit.preferences = preferences
            self.units.append(unit)
    
    def _create_instructors(self, data: List[dict]) -> None:
        for instructor_data in data:
            name = instructor_data['name']
            title = instructor_data['title']
            gender = instructor_data['gender']
            identifier = int(instructor_data['identifier'])
       
            preferences = self._create_preferences(instructor_data.get('preferences', []))
            
            instructor = Instructor(name, title, gender, identifier)
            instructor.preferences = preferences
            self.instructors.append(instructor)
    
    def _create_groups(self, data: List[dict]) -> None:
        
        for group_data in data:
            id_ = group_data['identifier']
            title = group_data['programme']
            year = group_data['year']
            total = group_data["total"]
            preferences = self._create_preferences(group_data.get('preferences', []))
            
            group = Group(id_, title, year)
            group.total = total
            group.preferences = preferences
            self.groups.append(group)
    
    def _create_preferences(self, data: List[dict] | None) -> Preferences:
        all_ = All()
        p = Preferences()
        p.AddRule(all_)
        return p

    def _create_rooms(self, data: List[dict]):
        for room_data in data:
            id_ = room_data["identifier"]
            name = room_data["name"]
            total = room_data["capacity"]
            preferences = self._create_preferences(room_data["preferences"])

            room = Room(id_, name, total)
            room.preferences = preferences
            self.rooms.append(room)

    def _create_configurations(self, data: dict):
        self.configuration = Configuration(data["name"], data["start_time"], data["end_time"], data["days"])

        self.configuration.duration_per_session = data["duration_per_session"]
        self.configuration.total_duration_for_sessions = data["total_duration_for_sessions"]

        self.configuration.consecutive = data["consecutive"]

        self.configuration.system = data["system"]
        self.configuration.soft_constraints_satisfaction_rate = data["soft_contraints_satisfaction_rate"]

        p = Priorities()
        p.define(data["priorities"]["room"], data["priorities"]["instructors"], data["priorities"]["units"], data["priorities"]["groups"])
        self.configuration.priorities = p