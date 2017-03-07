# encoding utf-8

from custom_errors import *
from toolbox import *
from pickle import *
import os


def find_entrance(maze):
    """
    Find 'E' in a list of string
    :param maze: the list of string to parse
    :return: a tuple with the coordinate of the entrance
    """
    for y, map_line in enumerate(maze):
        if 'X' in map_line:
            return str(map_line).index('X'), y


def find_exit(maze):
    """
    Find 'U' in a list of string
    :param maze: the list of string to parse
    :return: a tuple with the coordinate of the entrance
    """
    for y, map_line in enumerate(maze):
        if 'U' in map_line:
            return str(map_line).index('U'), y


class Maze:

    def __init__(self, map_drawing):

        if type(map_drawing) != list or len(map_drawing) <= 0:
            raise TypeError("Wrong type give")

        self.map = list(map_drawing)
        self.clean_map = list(map_drawing)
        self.size = self.len()
        self.exit_position = find_exit(self.map)
        self.robot_position = find_entrance(self.map)

        # Remove robot position from clean map
        robot_line = list(self.clean_map[self.robot_position[1]])
        robot_line[self.robot_position[0]] = " "
        self.clean_map[self.robot_position[1]] = "".join(robot_line)

    def __repr__(self):
        map_str = str()
        for map_line in self.map:
            map_str += map_line + "\r\n"
        return str(map_str)

    def len(self):
        """
        Function to get the dimension of the maze
        :return: the dimension of the maze
        """
        return len(self.map[0]), len(self.map)

    def update_robot_position(self, direction, step):
        """
        Update position of the robot into the maze
        :param direction: direction for the robot to move
        :param step: number of step to do
        """

        new_x, new_y = self.calculate_coordinate(direction, step)

        # -------------------------------
        # Delete previous robot position
        # -------------------------------
        self.map[self.robot_position[1]] = self.clean_map[self.robot_position[1]]

        # -------------------------------
        # Update robot position
        # -------------------------------
        map_list = list(self.map[new_y])
        map_list[new_x] = 'X'
        self.map[new_y] = "".join(map_list)

        self.robot_position = (new_x, new_y)

    def parse_command(self):
        """
        Parse the command given to mode
        :return: True if command valid, False otherwise
        """

        print("------------------------------------------")
        cmd = str(input("So, where does the robot go?\r\n")).upper()
        try:
            if len(cmd) <= 0:
                raise EmptyOptions(cmd)
            elif cmd[0] not in command_arguments:
                raise InvalidCommands(cmd)
            elif len(cmd) == 1 and cmd == "Q":
                    self.save()
                    exit(0)

        except EmptyOptions as e:
            print(e)
            print_cmd_usage()
            return -1, -1
        except InvalidCommands as e:
            print(e)
            print_cmd_usage()
            return -1, -1

        cmd_direction = cmd[0]
        if len(cmd) > 1:
            cmd_steps = int(cmd[1:])
        else:
            cmd_steps = 1

        if self.is_itinerary_clear(cmd_direction, cmd_steps):
            return cmd_direction, cmd_steps
        else:
            print_cmd_usage()
            return -1, -1

    def calculate_coordinate(self, direction, step):
        """
        Calculate new coordinate to move the robot
        :param direction: direction to move to
        :param step: number of step to move
        :return: tuple of the new coordinate, (-1, -1) if invalids coordinate
        """

        (x, y) = (-1, -1)
        if direction == "N":
            x, y = self.robot_position[0], self.robot_position[1] - step
        elif direction == "E":
            x, y = self.robot_position[0] + step, self.robot_position[1]
        elif direction == "S":
            x, y = self.robot_position[0], self.robot_position[1] + step
        elif direction == "W":
            x, y = self.robot_position[0] - step, self.robot_position[1]

        if x < 0 or y < 0 or x > self.len()[0] or y > self.len()[1]:
            raise CoordinateOutOfRange((x,y))

        return x, y

    def is_itinerary_clear(self, cmd_direction, cmd_steps):
        """
        Dry run the itinerary of robot and check if any obstacle
        :param cmd_direction: direction to follow
        :param cmd_steps: number of step in that direction
        :return: True if path is clean, False if and obstacles found
        """

        if type(cmd_direction) != str or type(cmd_steps) != int or cmd_steps < 0 or len(cmd_direction) != 1:
            return False

        try:
            self.calculate_coordinate(cmd_direction, cmd_steps)
        except CoordinateOutOfRange as e:
            print(e)
            return False

        itinerary = list()

        try:
            if cmd_direction == 'N':
                for i in range(0, cmd_steps + 1):
                    itinerary.append(self.map[(self.robot_position[1]) - i][self.robot_position[0]])
                if 'O' in itinerary:
                    raise EncounterObstacle(itinerary)

            elif cmd_direction == 'S':
                for i in range(0, cmd_steps + 1):
                    itinerary.append(self.map[(self.robot_position[1]) + i][self.robot_position[0]])
                if 'O' in itinerary:
                    raise EncounterObstacle(itinerary)

            elif cmd_direction == 'E':
                for i in range(0, cmd_steps + 1):
                    itinerary.append(self.map[self.robot_position[1]][self.robot_position[0] + i])
                if 'O' in itinerary:
                    raise EncounterObstacle(itinerary)

            elif cmd_direction == 'W':
                for i in range(0, cmd_steps + 1):
                    itinerary.append(self.map[self.robot_position[1]][self.robot_position[0] - i])
                if 'O' in itinerary:
                    raise EncounterObstacle(itinerary)

        except EncounterObstacle as e:
            print(e)
            return False

        except IndexError as e:
            print("You have encounter an obstacle with move {}{}".format(cmd_direction, cmd_steps))
            return False

        return True

    def is_maze_resolved(self):
        """
        Check if Robot found the exit
        :return: True if exit found, False otherwise
        """
        if self.robot_position == self.exit_position:
            return True
        else:
            return False

    def save(self, save_name):
        """
        Save the game in binary file name.sav and quit the game
        :param save_name : name of the game to save
        """
        confirm = True
        file_name = "{}.sav".format(self.name)
        print("File to save {}".format(file_name))

        if os.path.isfile(file_name):
            ret = str(input("Are you sure you want to erase save {}? (Y/N)\r\n".format(file_name)))
            while ret.upper() not in ("Y", "N"):
                ret = str(input("Are you sure you want to erase save {}? (Y/N)\r\n".format(file_name)))
            if ret.upper() == "N":
                confirm = False
            else:
                confirm = True

        if confirm:
            with open(file_name, 'wb') as save:
                my_pickler = Pickler(save)
                my_pickler.dump(self)
            print("File {} saved".format(file_name))
        exit()
