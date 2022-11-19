from itertools import count


class Passenger:
    __id_new = count(1)

    def __init__(self, current_floor: int, destination_floor: int) -> None:
        assert current_floor != destination_floor

        self._id: int = next(self.__id_new)
        self._current_floor: int = current_floor
        self._destination_floor: int = destination_floor

    def __repr__(self) -> str:
        return f'{self.id}:{self.destination_floor}'

    @property
    def id(self) -> int:
        return self._id

    @property
    def current_floor(self) -> int:
        return self._current_floor

    @property
    def destination_floor(self) -> int:
        return self._destination_floor
