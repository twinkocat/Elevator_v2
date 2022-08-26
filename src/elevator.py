from enum import Enum

from constants import FIRST_FLOOR, MAX_CAPACITY, MAX_FLOORS, ONE_FLOOR


class Elevator:
    class Direction(Enum):
        Stop = 0
        Down = 1
        Up = 2

    def __init__(self, current_floor=FIRST_FLOOR):

        self.max_capacity = MAX_CAPACITY
        self.current_floor = current_floor
        self.passengers = []
        self._direction = self.Direction.Stop

    def __repr__(self):
        return f'current_floor: {self.current_floor} | passengers: {[*self.passengers]}'

    @property
    def passengers_count(self):
        return len(self.passengers)

    @property
    def min_floor_target(self):
        if not self.passengers:
            self.direction = self.Direction.Stop  # elevator stopped and waiting call
            return 0
        else:
            return min([passenger.destination_floor for passenger in self.passengers])

    @property
    def max_floor_target(self):
        if not self.passengers:
            return 0
        else:
            return max([passenger.destination_floor for passenger in self.passengers])

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value == self.Direction.Up or self.Direction.Down or self.Direction.Stop:
            self._direction = value
        else:
            print(f"Value {value} is can`t be direction for elevator")

    def go_up(self):
        if self.current_floor < MAX_FLOORS:
            self.current_floor += ONE_FLOOR
            self.direction = self.Direction.Up
        else:
            self.direction = self.Direction.Stop

    def go_down(self):
        if self.current_floor > FIRST_FLOOR:
            self.current_floor -= ONE_FLOOR
            self.direction = self.Direction.Down
        else:
            self.direction = self.Direction.Stop

    def entire_passenger(self, floor):
        """This method are filter objects for entering to elevator"""

        # creating one list of three if the condition is met other do not write in "passengers_to_entire"

        passengers_to_entire = \
            [  # direction is Up
                passenger for passenger
                in floor.passengers_on_the_floor
                if passenger.destination_floor > self.current_floor
                and self.direction == self.Direction.Up][0: MAX_CAPACITY - self.passengers_count
            ] \
            or \
            [  # direction is Down
                passenger for passenger
                in floor.passengers_on_the_floor
                if passenger.destination_floor < self.current_floor
                and self.direction == self.Direction.Down][0: MAX_CAPACITY - self.passengers_count
            ] \
            or \
            [  # direction is None
                passenger for passenger
                in floor.passengers_on_the_floor
                if passenger.destination_floor != self.current_floor
                and self.direction == self.Direction.Stop][0: MAX_CAPACITY - self.passengers_count
            ] \
            or \
            [  # entire a passengers in last floor
                passenger for passenger
                in floor.passengers_on_the_floor
                if passenger.destination_floor != self.current_floor
                and self.current_floor == MAX_FLOORS][0: MAX_CAPACITY - self.passengers_count
            ]

        self.passengers.extend(passengers_to_entire)

        for passenger in passengers_to_entire:
            floor.passengers_on_the_floor.pop(floor.passengers_on_the_floor.index(passenger))

    def exit_passenger(self, floor):
        passengers_to_exit = [
            passenger for passenger in self.passengers if passenger.destination_floor == self.current_floor
        ]
        floor.passengers_on_the_floor += passengers_to_exit

        for passenger in passengers_to_exit:
            self.passengers.pop(self.passengers.index(passenger))

    def call_or_stop_elevator(self, floors):
        bool_list = []
        for floor in floors:
            passenger_destinations_floor = [passenger.destination_floor for passenger in
                                            floor.passengers_on_the_floor]
            for destination_floor in passenger_destinations_floor:
                if destination_floor == floor.floor:
                    bool_list.append(True)
                else:
                    bool_list.append(False)
                    self.current_floor = floor.floor
                    return bool_list
        return bool_list

