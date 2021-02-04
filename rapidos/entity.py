class Rapidos(object):
    def __init__(self, name: str):
        self.name = name
        self.rooms = []
        self.slots = []

    def duration_formatted(self):
        return 'TODO'

    def add_room(self, room_name: str):
        self.rooms.append(room_name)

    def add_slot(self, slot_start_time):
        self.slots.append(slot_start_time)
