from Assets.Formation.html import designHeader, designFooter


class Format:
    def __init__(self, text: list, type_="json"):
        self.result = None
        self.text = text
        self.type_ = type_
        self.form()

    def form(self):
        if self.type_ == "json":
            self.formJSON()
        elif self.type_ == "html":
            self.formHTML()

    def formJSON(self):
        self.result = []
        form = {}
        for i in self.text:
            form['identifier'] = i.schedule.identifier
            form['group'] = i.schedule.group.title
            form['year'] = i.schedule.group.year
            form['daytime'] = str(i.daytime)
            form['instructor'] = i.schedule.instructor.name
            form['unit'] = i.schedule.unit.title
            self.result.append(form)
            form = {}

    def formHTML(self):

        self.result = designHeader("Timetable Generator") + designFooter()

    def GiveResult(self):
        return self.result
