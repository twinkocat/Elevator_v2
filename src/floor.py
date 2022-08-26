
class Floor:

    def __init__(self, floor_number, passengers):
        self.floor = floor_number
        self.passengers_on_the_floor = passengers

    def __repr__(self):
        return f'|{self.floor} {self.passengers_on_the_floor}|'
