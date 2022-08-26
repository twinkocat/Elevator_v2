import time
from random import choice, randint

from constants import MIN_PASSENGERS, MAX_PASSENGERS, MAX_FLOORS
from src.elevator import Elevator
from src.floor import Floor
from src.passenger import Passenger


class House:

    def __init__(self):
        self.elevator = self.Elevator()
        self.floors = self.floors_create()

    class Floor(Floor):
        pass

    class Elevator(Elevator):
        pass

    class Passenger(Passenger):
        pass

    def floors_create(self) -> list:
        """Constructor for create House object with Floors and Passengers"""
        start_function = time.time()
        if MIN_PASSENGERS > MAX_PASSENGERS:
            raise Exception(f'{MIN_PASSENGERS} can be higher then {MAX_PASSENGERS}')

        """Service for create floors objects and passengers on this floor"""
        floors_list = []
        for current_floor in range(1, MAX_FLOORS + 1):
            floors_list.append(
                # generate floor
                self.Floor(
                    current_floor,
                    # generate passenger
                    [self.Passenger(
                        current_floor,
                        choice([destination_floor for destination_floor in range(1, MAX_FLOORS + 1)
                                if destination_floor != current_floor])
                    )
                        # generate random count of passengers in the floor
                        for passengers in range(randint(MIN_PASSENGERS, MAX_PASSENGERS))
                    ]
                )
            )
        end_function = time.time()
        print(f'function complete the house in {end_function - start_function} seconds')
        time.sleep(2)

        return floors_list
