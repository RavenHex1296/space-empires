import math
import random
import sys
sys.path.append('src')
from logger import *

random.seed(1)

class Game:
    def __init__(self, players, board_size=[7,7]):
        self.logs = Logger('/home/runner/space-empires/logs/game_level_0_3.txt')
        self.logs.clear_log()
        self.players = players
        self.set_player_numbers()
        self.combat_coords = {}

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

    def same_player_scouts(self, input_list):
        for n in range(len(input_list)):
            if n != 0:
                if input_list[n] != input_list[n - 1]:
                    return False

        return True

    def opponent_scout(self, p_num, combat_loc):
        for scout in combat_loc:
            if scout[0] != p_num:
                return scout

    def complete_combat_phase(self):
        if self.state['winner'] != None:
            return None

        self.logs.write("\nBEGINNING OF TURN " + str(self.state['turn']) + " COMBAT PHASE\n")

        if len(self.combat_coords) != 0:
            self.logs.write("\n\tCombat Locations:\n")

            for loc in self.combat_coords:
                self.logs.write("\n\t\t"+ str(loc) +"\n\n")

                for scout in self.combat_coords[loc]:
                    self.logs.write("\t\t\tPlayer "+ str(scout[0]) +" Scout "+ str(scout[1]) + "\n")

        delete_locs = []

        for loc in self.combat_coords:
            self.logs.write("\n\tCombat at " + str(loc) + "\n")


            while not self.same_player_scouts([scout[0] for scout in self.combat_coords[loc]]):

                for scout in self.combat_coords[loc]:
                    attacker = scout
                    defender = self.opponent_scout(scout[0], self.combat_coords[loc])

                    if defender == None:
                        break

                    self.logs.write("\n\t\tAttacker: Player " + str(scout[0]) + " Scout " + str(scout[1]))
                    self.logs.write("\n\t\tDefender: Player " + str(defender[0]) + " Scout " + str(defender[1]))

                    if round(random.random()) == 0:
                        self.logs.write("\n\t\t(Miss)\n")
                        continue

                    self.logs.write("\n\t\tHit!")
                    self.combat_coords[loc].remove(defender)
                    del self.state['players'][defender[0]]['scout_coords'][defender[1]]
                    self.logs.write("\n\t\tPlayer " + str(defender[0])+" Scout "+ str(defender[1]) + " was destroyed\n")

            self.logs.write("\n\tSurvivors:\n")
            self.logs.write("\n\t\t" + str(loc) + "\n")

            for scout in self.combat_coords[loc]:
                self.logs.write("\n\t\t\tPlayer " + str(scout[0]) + " Scout " + str(scout[1]))

            delete_locs.append(loc)
            self.logs.write('\n')

        for loc in delete_locs:
            del self.combat_coords[loc]

        self.logs.write("\nEND OF TURN " + str(self.state['turn']) + " COMBAT PHASE\n")

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

        if any(loc == p2_base for loc in p1_loc) and any(loc == p1_base for loc in p2_loc):
            self.logs.write("\nTIE GAME")
            self.state['winner'] = "Tie"


    def complete_movement_phase(self):
        if self.state['winner'] != None:
            return None

        self.logs.write("\nBEGINNING OF TURN " + str(self.state['turn']) + " MOVEMENT PHASE\n\n")

        for p_num in self.state['players']:
            p_scouts = self.state['players'][p_num]['scout_coords']
            op_scouts = self.state['players'][3 - p_num]['scout_coords']
            frozen_scouts = [loc for key in self.combat_coords for loc in self.combat_coords[key]]

            for scout_num in p_scouts:
                if (p_num, scout_num) in frozen_scouts:
                    continue

                scout = p_scouts[scout_num]
                choices = self.get_in_bounds_translations(scout)
                player = self.players[p_num - 1]
                choice = player.choose_translation(self.state, choices, scout_num)
                updated_locs = (scout[0] + choice[0], scout[1] + choice[1])

                self.state['players'][p_num]['scout_coords'][scout_num] = updated_locs
                self.logs.write('\tPlayer ' + str(p_num) + ' Scout ' + str(scout_num) + ': ' + str(scout) + ' -> ' + str(updated_locs) + '\n')

                for scout in op_scouts:
                    if op_scouts[scout] == updated_locs and updated_locs not in self.combat_coords:
                        self.combat_coords[updated_locs] = [(3-p_num, scout)]

                    elif op_scouts[scout]== updated_locs and updated_locs in self.combat_coords:
                        if (3 - p_num, scout) not in self.combat_coords[updated_locs]:
                            self.combat_coords[updated_locs].append((3 - p_num, scout))

                if updated_locs in self.combat_coords:
                    self.combat_coords[updated_locs].append((p_num, scout_num))

        self.logs.write("\nEND OF TURN " + str(self.state['turn']) + " MOVEMENT PHASE\n")

    def run_to_completion(self):
        while self.state['winner'] == None:
            self.complete_movement_phase()
            self.complete_combat_phase()
