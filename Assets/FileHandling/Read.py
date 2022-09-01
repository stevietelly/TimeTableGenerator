import json


class Read:
    def __init__(self, filename: str):
        self.fn = filename

    def extract(self):
        file = open(self.fn).read()
        content = json.loads(file)
        return content
