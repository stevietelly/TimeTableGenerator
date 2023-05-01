from typing import List
from Objects.User.Preferences.Rules import Rule



class Preferences:
    def __init__(self) -> None:
       """A preference is made up of a list of rules"""
       self.rules: List[Rule] = []
    
    def AddRule(self, rule:Rule):
        self.rules.append(rule)
    


