import math
import random

class PauseStrategy():
    def __init__(self):
        self.counter = 0

    def calculate_distance(self, initial_point, ending_point):
        x = ending_point[0] - initial_point[0]
        y = ending_point[1] - initial_point[1]
        return (x ** 2 + y ** 2) ** 0.5

    def min_distance_choice(self, choices, coordinate):
        best_choice = choices[0]
        min_distance = self.calculate_distance(best_choice, coordinate)

        for choice in choices:
            if self.calculate_distance(choice, coordinate) < min_distance:
                best_choice = choice
                min_distance = self.calculate_distance(choice, coordinate)

        return best_choice

    def min_distance_translation(self, choices, coordinate, desired_location):
        best_choice = choices[0]
        updated_coordinate = self.list_add(best_choice, coordinate)
        dist = self.calculate_distance(updated_coordinate, desired_location)

        for choice in choices:
            new_coordinate = [choice[i]+coordinate[i] for i in range(len(choice))]

            if self.calculate_distance(new_coordinate, desired_location) < dist:
                best_choice = choice
                updated_coordinate = new_coordinate
                dist = self.calculate_distance(new_coordinate, desired_location)

        return best_choice
    
    def list_add(self, x, y):
        return [x[i]+y[i] for i in range(len(x))]

    def select_translation(self, ship_coords, choices, opp_home_cols):
        if self.counter < 6:
            self.counter += 1
            return (0,0)
        closest_col = self.min_distance_choice(opp_home_cols, ship_coords)
        return self.min_distance_translation(choices, ship_coords, closest_col)
    
    def select_target(self, opponents):
        if len(opponents) == 1:
            return opponents[0]

        return opponents[random.randint(0, len(opponents) - 1)]
