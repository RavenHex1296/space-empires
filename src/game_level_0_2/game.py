import math
import random
import sys
sys.path.append('src')
from logger import *

class Game:
    def __init__(self, players, board_size=[7,7]):
        self.logs = Logger('/home/runner/space-empires/logs/game_level_0_2-log.txt')
        self.logs.clear_log()
        self.players = players
        self.set_player_numbers()

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': {
                        1: (mid_x, 1),
                        2: (mid_x, 1),
                        3: (mid_x, 1),
                    },
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': {
                        1: (mid_x, board_y),
                        2: (mid_x, board_y),
                        3: (mid_x, board_y),
                    },
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
        if self.state['winner'] != None:
            return None

        self.logs.write("\nBEGINNING OF TURN " + str(self.state['turn']) + " COMBAT PHASE\n")

        p1_scouts = self.state['players'][1]['scout_coords']
        p2_scouts = self.state['players'][2]['scout_coords']
        locs = []

        for scout1 in p1_scouts:
            for scout2 in p2_scouts:
                if p1_scouts[scout1] == p2_scouts[scout2]:
                    if p1_scouts[scout1] not in locs:
                        locs.append(p1_scouts[scout1])

        for loc in locs:
            self.logs.write("\n\tCombat at " + str(loc) + ":\n")
            p1_coord_scouts = [key for key in p1_scouts if p1_scouts[key]==loc]
            p2_coord_scouts = [key for key in p2_scouts if p2_scouts[key]==loc]

            while len(p1_coord_scouts)!=0 and len(p2_coord_scouts)!=0:
                winner = round(random.random()) + 1
                loser = 3 - winner
                if loser == 1:
                    lost_scout = random.choice(p1_coord_scouts)
                    p1_coord_scouts.remove(lost_scout)
                    del self.state['players'][loser]['scout_coords'][lost_scout]
                    self.logs.write("\n\t\tPlayer 1 Scout " + str
                    (lost_scout) + " was destroyed")

                elif loser == 2:
                    lost_scout = random.choice(p2_coord_scouts)
                    p2_coord_scouts.remove(lost_scout)
                    del self.state['players'][loser]['scout_coords'][lost_scout]
                    self.logs.write("\n\t\tPlayer 2 Scout " + str
                    (lost_scout) + " was destroyed")

        self.logs.write("\n" + "\nEND OF TURN " + str(self.state['turn']) + " COMBAT PHASE\n" + '-' * 50)

        self.state['turn'] += 1
        p1_scouts = self.state['players'][1]['scout_coords']
        p1_base = self.state['players'][1]['home_colony_coords']
        p2_scouts = self.state['players'][2]['scout_coords']
        p2_base = self.state['players'][2]['home_colony_coords']
        p1_loc = [p1_scouts[key] for key in p1_scouts]
        p2_loc = [p2_scouts[key] for key in p2_scouts]

        if not any(loc == p2_base for loc in p1_loc) and not any(loc == p1_base for loc in p2_loc):
            self.state['winner'] = None

        if any(loc == p2_base for loc in p1_loc) and not any(loc == p1_base for loc in p2_loc):
            self.logs.write("\nWINNER: PLAYER 1")
            self.state['winner'] = 1

        if not any(loc == p2_base for loc in p1_loc) and any(loc == p1_base for loc in p2_loc):
            self.logs.write("\nWINNER: PLAYER 2")
            self.state['winner'] = 2

        if any(loc==p2_base for loc in p1_loc) and any(loc==p1_base for loc in p2_loc):
            self.logs.write("\nTIE GAME")
            self.state['winner'] = "Tie"


    def complete_movement_phase(self):
        if self.state['winner'] != None:
            return None

        self.logs.write("\nBEGINNING OF TURN " + str(self.state['turn']) + " MOVEMENT PHASE\n\n")

        for player_num in self.state['players']:
            p1 = self.state['players'][1]
            p2 = self.state['players'][2]
            frozen_scouts = []

            for scout1 in p1['scout_coords']:
                scout1 = p1['scout_coords'][scout1]

                for scout2 in p2['scout_coords']:
                    scout2 = p2['scout_coords'][scout2]

                    if scout1 == scout2 and (1, scout1) not in frozen_scouts:
                        frozen_scouts.append((1, scout1))

                    if scout1 == scout2 and (2, scout2) not in frozen_scouts:
                        frozen_scouts.append((2, scout2))

            scouts = self.state['players'][player_num]['scout_coords']

            for scout_num in scouts:
                scout = scouts[scout_num]

                if (player_num,scout_num) not in frozen_scouts:
                    choices = self.get_in_bounds_translations(scout)
                    player = self.players[player_num - 1]
                    move = player.choose_translation(self.state, choices, scout_num)
                    self.state['players'][player_num]['scout_coords'][scout_num] = (scout[0] + move[0], scout[1] + move[1])

                self.logs.write("\tPlayer " + str(player_num) + " Scout " + str(scout_num) + ": " + str(scout) + " -> " + str((scout[0] + move[0], scout[1] + move[1])) + "\n")

        self.logs.write("\nEND OF TURN " + str(self.state['turn']) + " MOVEMENT PHASE\n" + "-" * 50)

    def run_to_completion(self):
        while self.state['winner'] == None:
            self.complete_movement_phase()
            self.complete_combat_phase()
