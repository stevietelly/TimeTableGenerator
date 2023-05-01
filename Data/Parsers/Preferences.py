from typing import Union
from Logic.DateTime.Day import Day
from Objects.User.Preferences.Rules import *
from Logic.DateTime.Time import Time
from Logic.DateTime.DayTime import DayTime
from Objects.Physical.Rooms import Room

class PreferenceParser:
    """
    Parses a string preference representation into a corresponding Rule object.

    Preference syntax:
    {QUALITY [TYPE:->'VALUE'] AND/OR [QUALITY [TYPE:->'VALUE'] AND/OR ...]}
    where
    - QUALITY: Before, After, Except, All, Only
    - TYPE: DAY, TIME, ROOM, DAYTIME
    - VALUE: the value of the TYPE
    """

    def __init__(self):
        self.quality_mapping = {
            "before": Before,
            "after": After,
            "all": All,
            "only": Only,
            "except": Except,
            "and": And,
            "or": Or
        }

    def parse_preference_string(self, preference_str: str) -> Union[Rule, Conjuction]:
        """
        Parses a preference string and returns a corresponding Rule or Conjuction object.
        :param preference_str: The preference string to parse.
        :return: A Rule or Conjuction object representing the preference string.
        """
        if preference_str.startswith('{') and preference_str.endswith('}'):
            print("here")
            # Strip the braces from the string.
            preference_str = preference_str[1:-1]

            # Split the string into rules and conjuctions.
            # rule_strings = preference_str.split(' AND ')
            # conjuction_strings = preference_str.split(' OR ')

            # If the preference string contains no conjuctions, it must be a rule.
            if not " AND " in preference_str and not " OR " in preference_str:
                # rule_str = conjuction_strings[0]
                if 'BEFORE' in preference_str:
                    value_str = preference_str.split('BEFORE ')[1]
                    return Before(self.parse_sub_string(value_str))
                elif 'AFTER' in preference_str:
                    value_str = preference_str.split('AFTER ')[1]
                    return After(self.parse_sub_string(value_str))
                elif 'ALL' in preference_str:
                    return All()
                elif 'EXCEPT' in preference_str:
                    value_str = preference_str.split('EXCEPT ')[1]
                    return Except(self.parse_sub_list(value_str))
                elif 'ONLY' in preference_str:
                    value_str = preference_str.split('ONLY ')[1]
                   
                    return Only(self.parse_sub_list(value_str))

            # If the preference string contains conjuctions, it must be a conjuction.
            else:
                
                if ' AND ' in preference_str:
                    rule_strings = preference_str.split(" AND ")
                    primary = self.parse_preference_string(rule_strings[0])
                    secondary = self.parse_preference_string(rule_strings[1])
                    return And(primary, secondary)
                elif ' OR ' in preference_str:
                    rule_strings = preference_str.split(" OR ")
                    
                    primary = self.parse_preference_string(rule_strings[0])
                    secondary = self.parse_preference_string(rule_strings[1])
                    return Or(primary, secondary)

        raise ValueError(f"Invalid preference string: {preference_str}")
    

    def parse_sub_string(self, rule_string:str):
        """
        Parses a string inside square brackets and returns the appropriate rule object.

        Args:
            rule_string (str): String representing a rule, e.g. "TIME:->'4:00PM'".

        Returns:
            Rule: A Rule object.

        Raises:
            ValueError: If the rule type is not recognized.
        """
        if not rule_string[0] == "[" and not rule_string[-1] == "]":
            raise ValueError(f"Unrecognized rule type '{rule_type}'")
        rule_string = rule_string.replace("[", "")
        rule_string = rule_string.replace("]", "")

        parts = rule_string.split(":->")
        rule_type = parts[0].upper()
        value = parts[1].strip("'")

        if rule_type == "TIME":
            return Time(value)
        elif rule_type == "DAY":
            return Day(value, Time("0:00"), Time("0:00"))
        elif rule_type == "ROOM":
            return Room(value, None, None)
        elif rule_type == "DAYTIME":
            v = value.split(" at ")
            day = Day(v[0], Time("0:00"), Time("0:00"))
            time = Time(v[1])
            return DayTime(day, time)
        else:
            raise ValueError(f"Unrecognized rule type '{rule_type}'")
        
    def parse_sub_list(self, rule_list:str):
        values = rule_list.split(", ")
        return_list = []
        for value in values:
            return_list.append(self.parse_sub_string(value))
        return return_list

