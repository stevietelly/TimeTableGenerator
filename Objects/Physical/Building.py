class Building:
    title = str

    no_of_rooms = 0
    rooms = []

    def __init__(self, title: str):
        self.title = title

    def __repr__(self):
        return self

    def __str__(self):
        return f'{self.title}->{self.no_of_rooms} classes(s)'

    def AddRoom(self, room):
        self.rooms.append(room)
        self.no_of_rooms += 1
