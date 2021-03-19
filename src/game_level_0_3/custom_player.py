from random import random

def distance(initial_point, ending_point):
    x = ending_point[0] - initial_point[0]
    y = ending_point[1] - initial_point[1]
    return (x ** 2 + y ** 2) ** 0.5

class CustomPlayer():
    def __init__(self):
        self.player_number = None

    def set_player_number(self, n):
        self.player_number = n

    def get_opponent_player_number(self):
        if self.player_number == None:
            return None

        elif self.player_number == 1:
            return 2

        elif self.player_number == 2:
            return 1

    def choose_translation(self, game_state, choices, scout_num):
        myself = game_state['players'][self.player_number]
        opponent_player_number = self.get_opponent_player_number()
        opponent = game_state['players'][opponent_player_number]

        my_scout_coords = myself['scout_coords'][scout_num]
        opponent_home_colony_coords = opponent['home_colony_coords']

        closest_choice = choices[0]
        smallest_distance_coordinates = (my_scout_coords[0] + closest_choice[0], my_scout_coords[1] + closest_choice[1])
        smallest_distance = distance(smallest_distance_coordinates, opponent_home_colony_coords)

        for choice in choices:
            updated_coordinates = (my_scout_coords[0] + choice[0], my_scout_coords[1] + choice[1])

            if distance(updated_coordinates, opponent_home_colony_coords) < smallest_distance:
                closest_choice = choice
                smallest_distance = distance(updated_coordinates, opponent_home_colony_coords)

        return closest_choice
