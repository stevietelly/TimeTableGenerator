
class Format:
    result = []

    def __init__(self, text: list, type_):
        self.text = text
        self.type_ = type_
        self.form()

    def form(self):
        pass

    def GiveResult(self):
        return self.result
