try:
    import curses
except ModuleNotFoundError:
    from sys import platform

    if platform == "win32":
        print("EXCEPTION!: Module curses not found.\n"
              "Need install module curses: pip install windows-curses")

import time

from constants import INTERVAL_FOR_UPDATE, MAX_CAPACITY, MAX_FLOORS
from src.house import obj_house


def scenario_executor(house: obj_house) -> None:
    my_screen = curses.initscr()
    while True:
        time.sleep(INTERVAL_FOR_UPDATE)

        floor = [floor for floor in house.floors if floor.floor == house.elevator.current_floor]

        #########################################################################################################
        #                                                 GUI                                                   #
        #                                         Run this in PyCharm:                                          #
        # Run -> Edit Configurations...-> Executions -> toggle on "Emulate terminal in output console" -> Apply #
        #                                  curses only working into console...                                  #
        #                                                                                                       #
        my_screen.clear()  #
        my_screen.border(0)  #
        #                                                                                                       #
        #                                              elevator GUI                                             #
        my_screen.addstr(2, 23, "|floor|")  #
        my_screen.addstr(3, 24, f'>|{house.elevator.current_floor}|<')  #
        my_screen.addstr(4, 18, f'direction is {house.elevator.direction.name}')  #
        my_screen.addstr(5, 16, f' min target floor {house.elevator.min_floor_target}')  #
        my_screen.addstr(6, 16, f' max target floor {house.elevator.max_floor_target}')  #
        #                                                                                                       #
        #                                               House GUI                                               #
        my_screen.addstr(7, 1, f' Flour    |    Elevator have {house.elevator.passengers_count} passengers'  #
                               f'               | Passengers [id : destination floor]')  #
        #                                                                                                       #
        for floor_element in range(MAX_FLOORS):  #
            my_screen.addstr(8 + floor_element, 4, f'{floor_element + 1}')  #
            my_screen.addstr(7 + house.elevator.current_floor, 11, f'| {house.elevator.passengers} |')  #
            my_screen.addstr(8 + floor_element, 57,  #
                             f'| {[floor for floor in house.floors if floor.floor == floor_element + 1]}')  #
            #
        my_screen.refresh()  #
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

        if house.elevator.passengers_count == 0 and house.elevator.direction == house.elevator.Direction.Stop:
            bool_list = house.elevator.call_or_stop_elevator(house.floors)
            if False in bool_list:
                bool_list.clear()
            else:
                my_screen.addstr(3, 40, "DONE! Turn any key to exit.")
                break
    my_screen.getch()
    curses.endwin()


if __name__ == '__main__':
    scenario_executor(obj_house)