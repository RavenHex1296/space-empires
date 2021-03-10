import random
import math

class Game:
    def __init__(self, players, random_seed, board_size=[7,7]):
        self.players = players
        self.set_player_numbers()
        random.seed(random_seed)

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': (mid_x, 1),
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': (mid_x, board_y),
                    'home_colony_coords': (mid_x, board_y)
                }
            },
            'winner': None
        }

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        board_x, board_y = self.state['board_size']

        if 1 <= x and x <= board_x:
            if 1 <= y and y <= board_y:
                return True

        return False

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.state['board_size']
        x, y = coords
        dx, dy = translation
        new_coords = (x+dx,y+dy)
        return self.check_if_coords_are_in_bounds(new_coords)

    def get_in_bounds_translations(self, coords):
        translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = []

        for translation in translations:
            if self.check_if_translation_is_in_bounds(coords, translation):
                in_bounds_translations.append(translation)

        return in_bounds_translations

    def complete_combat_phase(self):
        p1 = self.state['players'][1]
        p2 = self.state['players'][2]

        if p1['scout_coords'] == p2['scout_coords']:
            winner = round(random.random()) + 1
            loser = 3 - winner
            self.state['players'][loser]['scout_coords'] = None

    def complete_movement_phase(self):
        for p_num in self.state['players']:
            if self.state['players'][1]['scout_coords'] == self.state['players'][2]['scout_coords']:
                break

            elif self.state['players'][p_num]['scout_coords'] != None:
                initial_coordinates = self.state['players'][p_num]['scout_coords']
                choices = self.get_in_bounds_translations(initial_coordinates)

                for player in self.players:
                    if player.player_number == p_num:
                        move = player.choose_translation(self.state, choices)

                self.state['players'][p_num]['scout_coords'] = (initial_coordinates[0] + move[0], initial_coordinates[1] + move[1])

        self.state['turn'] += 1

        p1 = self.state['players'][1]
        p2 = self.state['players'][2]

        if p1['scout_coords'] != p2['home_colony_coords'] and p2['scout_coords'] != p1['home_colony_coords']:
            self.state['winner'] = None

        elif p1['scout_coords'] == p2['home_colony_coords'] and p2['scout_coords'] != p1['home_colony_coords']:
            self.state['winner'] =  1

        elif p1['scout_coords'] != p2['home_colony_coords'] and p2['scout_coords']== p1['home_colony_coords']:
            self.state['winner'] =  2

        elif p1['scout_coords'] == p2['home_colony_coords'] and p2['scout_coords'] == p1['home_colony_coords']:
            self.state['winner'] =  "Tie"


    def run_to_completion(self):
        while self.state['winner'] == None:
            self.complete_movement_phase()
            self.complete_combat_phase()
