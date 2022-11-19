
class Floor:

    def __init__(self, floor_number, passengers) -> None:
        self.floor: int = floor_number
        self.passengers_on_the_floor: list = passengers

    def __repr__(self) -> str:
        return f'|{self.floor} {self.passengers_on_the_floor}|'
