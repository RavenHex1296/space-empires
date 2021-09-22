import sys
sys.path.append('src')
import random
from colony import *


class CustomPlayer():
    def __init__(self):
        self.player_number = None
        self.ships = []
        self.home_colony = None
        self.colonies = []

    def calculate_distance(self, initial_point, ending_point):
        x = ending_point[0] - initial_point[0]
        y = ending_point[1] - initial_point[1]
        return (x ** 2 + y ** 2) ** 0.5
    
    def add_ship(self, ships):
        self.ships.append(ships)
    
    def set_home_colony(self, coordinates):
        self.home_colony = Colony(self.player_number, coordinates)
    
    def add_colonies(self, colonies):
        for colony in colonies:
            self.colonies.append(col)

    def set_player_number(self, n):
        self.player_number = n

    def get_opponent_player_number(self):
        if self.player_number == None:
            return None

        elif self.player_number == 1:
            return 2

        elif self.player_number == 2:
            return 1

    def get_best_option(self, options, coordinate):
        best_option = options[0]
        least_distance = self.calculate_distance(best_option, coordinate)

        for option in options:
            if self.calculate_distance(option, coordinate) < least_distance:
                best_option = option
                least_distance = self.calculate_distance(option, coordinate)

        return best_option

    def get_best_translation(self, options, coordinate, desired_location): #will need to rename desired_location to something else later, meant to mean enemy home colony location but not sure how to keep general for now
        best_option = options[0]
        updated_coordinate = [best_option[n] + coordinate[n] for n in range(len(best_option))]
        least_distance = self.calculate_distance(updated_coordinate, desired_location)

        for option in options:
            possible_translation = [option[n]+coordinate[n] for n in range(len(option))]

            if self.calculate_distance(possible_translation, desired_location) < least_distance:
                best_option = option
                updated_coordinate = possible_translation
                least_distance = self.calculate_distance(possible_translation, desired_location)

        return best_option

    def select_translation(self, coordinates, options, desired_location):
        best_option = self.get_best_option(desired_location, coordinates)
        return self.get_best_translation(options, coordinates, best_option)

    def select_target(self, options):
        if len(options) == 1:
            return enemies[0]

        return enemies[random.randint(0, len(enemies) - 1)]
