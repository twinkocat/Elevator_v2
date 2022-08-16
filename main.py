import curses
import itertools
import time
from random import randint, choice


# DO NOT TOUCH THIS PLS :3
FIRST_FLOOR = 1
ONE_FLOOR = 1

# config min and max floors
MAX_FLOORS = randint(5, 20)

# config min and max passengers on the floor
MIN_PASSENGERS = 0
MAX_PASSENGERS = 10

# config max capacity of elevator
MAX_CAPACITY = 5

# loop update interval
INTERVAL_FOR_UPDATE = 0.65


class House:

    def __init__(self, floors):
        self.elevator = self.Elevator()
        self.floors: list = floors

    class Floor:

        def __init__(self, floor_number, passengers):
            self.floor = floor_number
            self.passengers_on_the_floor = passengers

        def __repr__(self):
            return f'|{self.floor} {self.passengers_on_the_floor}|'

    class Elevator:

        def __init__(self, current_floor=FIRST_FLOOR, direction="None"):

            self.max_capacity = MAX_CAPACITY
            self.current_floor = current_floor
            self.passengers = []
            self._direction = direction

        def __repr__(self):
            return f'current_floor: {self.current_floor} | passengers: {[*self.passengers]}'

        @property
        def passengers_count(self):
            return len(self.passengers)

        @property
        def min_floor_target(self):
            if not self.passengers:
                self.direction = "None"  # elevator stopped and waiting call
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
            if value == "Up" or "Down" or "None":
                self._direction = value
            else:
                print(f"Value {value} is can`t be direction for elevator")

        def go_up(self):
            if self.current_floor < MAX_FLOORS:
                self.current_floor += ONE_FLOOR
                self.direction = "Up"
            else:
                self.direction = "None"

        def go_down(self):
            if self.current_floor > FIRST_FLOOR:
                self.current_floor -= ONE_FLOOR
                self.direction = "Down"
            else:
                self.direction = "None"

        def entire_passenger(self, floor):
            """This method are filter objects for entering to elevator"""

            # creating one list of three if the condition is met other do not write in "passengers_to_entire"

            passengers_to_entire = \
                [  # direction is Up
                    passenger for passenger
                    in floor.passengers_on_the_floor
                    if passenger.destination_floor > self.current_floor
                    and self.direction == "Up"][0: MAX_CAPACITY - self.passengers_count
                ] \
                or \
                [  # direction is Down
                    passenger for passenger
                    in floor.passengers_on_the_floor
                    if passenger.destination_floor < self.current_floor
                    and self.direction == "Down"][0: MAX_CAPACITY - self.passengers_count
                ] \
                or \
                [  # direction is None
                    passenger for passenger
                    in floor.passengers_on_the_floor
                    if passenger.destination_floor != self.current_floor
                    and self.direction == "None"][0: MAX_CAPACITY - self.passengers_count
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

    class Passenger:
        __id_new = itertools.count(1)

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


def floors_create(house_floor, passenger, max_floors: int = MAX_FLOORS):
    if MIN_PASSENGERS > MAX_PASSENGERS:
        raise Exception(f'{MIN_PASSENGERS} can be higher then {MAX_PASSENGERS}')

    """Service for create floors objects and passengers on this floor"""
    floors_list = []
    for current_floor in range(1, max_floors + 1):
        floors_list.append(
            # generate floor
            house_floor(
                current_floor,
                # generate passenger
                [passenger(
                    current_floor,
                    choice([i for i in range(1, max_floors + 1) if i != current_floor])
                )
                    # generate random count of passengers in the floor
                    for x in range(randint(MIN_PASSENGERS, MAX_PASSENGERS))
                ]
            )
        )
    return floors_list


def executor(house):
    while True:
        time.sleep(INTERVAL_FOR_UPDATE)

        floor = [floor for floor in house.floors if floor.floor == house.elevator.current_floor]

        #########################################################################################################
        #                                                 GUI                                                   #
        #                                         Run this in PyCharm:                                          #
        # Run -> Edit Configurations...-> Executions -> toggle on "Emulate terminal in output console" -> Apply #
        #                                  curses only working into console...                                  #
        #                                                                                                       #
        my_screen.clear()                                                                                       #
        my_screen.border(0)                                                                                     #
        #                                                                                                       #
        #                                              elevator GUI                                             #
        my_screen.addstr(2, 23, "|floor|")                                                                      #
        my_screen.addstr(3, 24, f'>|{house.elevator.current_floor}|<')                                          #
        my_screen.addstr(4, 18, f'direction is {house.elevator.direction}')                                     #
        my_screen.addstr(5, 16, f' min target floor {house.elevator.min_floor_target}')                         #
        my_screen.addstr(6, 16, f' max target floor {house.elevator.max_floor_target}')                         #
        #                                                                                                       #
        #                                               House GUI                                               #
        my_screen.addstr(7, 1, f' Flour    |    Elevator have {house.elevator.passengers_count} passengers'     #
                               f'               | Passengers [id : destination floor]')                         #
        #                                                                                                       #
        for floor_element in range(MAX_FLOORS):                                                                 #
            my_screen.addstr(8 + floor_element, 4, f'{floor_element + 1}')                                      #
            my_screen.addstr(7 + house.elevator.current_floor, 11, f'| {house.elevator.passengers} |')          #
            my_screen.addstr(8 + floor_element, 57,                                                             #
                             f'| {[floor for floor in house.floors if floor.floor == floor_element + 1]}')      #
                                                                                                                #
        my_screen.refresh()                                                                                     #
        #                                                                                                       #
        #########################################################################################################

        if house.elevator.passengers_count <= MAX_CAPACITY \
                or house.elevator.current_floor == house.elevator.min_floor_target:
            house.elevator.exit_passenger(*floor)
            house.elevator.entire_passenger(*floor)

        if house.elevator.min_floor_target > house.elevator.current_floor:
            house.elevator.go_up()
        else:
            house.elevator.go_down()

        if house.elevator.passengers_count == 0 and house.elevator.direction == "None":
            bool_list = house.elevator.call_or_stop_elevator(house.floors)
            if False in bool_list:
                bool_list.clear()
            else:
                my_screen.addstr(3, 40, "DONE! Turn any key to exit.")
                break


if __name__ == '__main__':
    # create object House from service
    house = House(
        floors_create(House.Floor, House.Passenger)
    )

    my_screen = curses.initscr()

    # execute!
    executor(house)

    my_screen.getch()

    curses.endwin()
