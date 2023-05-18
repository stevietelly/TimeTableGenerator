from typing import Any
import sys
import termcolor

class Echo:
    state: bool = False
    def __init__(self) -> None:
        """
        A class to approve printing specific values to the screen
        """
        pass
    def print(self, *value: Any, color=None):
        if self.state:
            print(*value) if not color else termcolor.cprint(f'{str(*value)}', color)
   
    def exit(self, error_string, error_value=2):
        termcolor.cprint(f'{str(error_string)}', "red")
        sys.exit(error_value)
