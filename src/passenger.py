from itertools import count


class Passenger:
    __id_new = count(1)

    def __init__(self, current_floor, destination_floor):
        assert current_floor != destination_floor

        self._id = next(self.__id_new)
        self._current_floor = current_floor
        self._destination_floor = destination_floor

    def __repr__(self):
        return f'{self.id}:{self.destination_floor}'

    @property
    def id(self):
        return self._id

    @property
    def current_floor(self):
        return self._current_floor

    @property
    def destination_floor(self):
        return self._destination_floor
