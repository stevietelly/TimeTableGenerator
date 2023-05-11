from typing import Callable



class Loop:
    def __init__(self, call: Callable[..., None], times: int, *args) -> None:
        """
        A looping structure to allow calls to be excuted a number of times.
        """
        self.call = call
        self.times = times
        self.args = args

    def Loop(self):
      for i in range(self.times):
            try:
                self.call(*self.args)
            except Exception as e:
                print(f"An error occurred: {e}")