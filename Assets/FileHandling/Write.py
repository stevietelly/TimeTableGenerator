import json


class Write:
    def __init__(self, filename, content):
        self.fn = filename
        self.cont = content

    def dump(self):
        d = json.dumps(self.cont, indent=1)
        with open(self.fn, 'w') as f:
            f.write(d)
