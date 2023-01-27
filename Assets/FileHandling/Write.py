import json


class Write:
    def __init__(self, filepath, filename, content, type_="json"):
        self.fn = filename
        self.cont = content
        self.type_ = type_
        self.fp = filepath

    def dump(self):
        if self.type_ == "json":
            self.dumpJSON()
        elif self.type_ == "html":
            self.dumpHTML()

    def dumpJSON(self):
        d = json.dumps(self.cont, indent=1)
        with open(self.fp + self.fn, 'w') as f:
            f.write(d)

    def dumpHTML(self):
        # create stylesheet
        open(f'{self.fp}/css/style.css', 'w')
        f = open(self.fp + self.fn, 'w')
        f.write(self.cont)
