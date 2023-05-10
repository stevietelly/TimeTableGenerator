from typing import Any

class Echo:
    state: bool = False
    def __init__(self) -> None:
        """
        A class to approve printing specific values to the screen
        """
        pass
    def print(self, *value: Any):
        if self.state:
            print(*value)
