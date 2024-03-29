import math
import sys
import random
sys.path.append('src')
from logger import *
from ship import *
from ship_data import *
from colony import *

class Game:
    def __init__(self, players, board_size=[7,7], max_turns=100, initial_cp=150):
        self.logs = Logger('/workspace/space-empires/logs/game_version_1.txt')
        self.logs.clear_log()
        self.players = players
        self.set_player_numbers()
        self.board_size = board_size
        self.combat_coordinates = []
        self.max_turns = max_turns
        self.initial_cp = initial_cp
 
        global board_x, board_y, mid_x, mid_y
        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.board = {(x, y): [] for x in range(board_x) for y in range(board_y)}
        self.turn = 0
        self.winner = None
 
        self.initialize_game()
        self.get_simple_board()

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)
 
    def check_if_coordinates_are_in_bounds(self, coordinates):
        if coordinates == None:
            return False

        x, y = coordinates
        board_x, board_y = self.board_size

        if 0 <= x and x < board_x:
            if 0 <= y and y < board_y:
                return True

        return False
 
    def check_if_translation_is_in_bounds(self, coordinates, translation):
        x, y = coordinates
        dx, dy = translation
        translation = (x + dx, y + dy)
        return self.check_if_coordinates_are_in_bounds(translation)

    def get_in_bounds_translations(self, coordinates):
        translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = []
 
        for translation in translations:
            if self.check_if_translation_is_in_bounds(coordinates, translation):
                in_bounds_translations.append(translation)
 
        return in_bounds_translations

    def is_enemy_in_translation(self, ship):
        enemy_present = False

        for item in self.board[ship.coords]:
            if item.player_num != ship.player_num:
                if ship.coords not in self.combat_coordinates and isinstance(ship, Ship) and isinstance(item, Ship):
                    self.combat_coordinates.append(ship.coords)
                    enemy_present = True


        return enemy_present

    def add_to_board(self, objects, coordinates):
        if type(objects) is not list:
            objects = [objects]

        for obj in objects:
            if obj.coords not in list(self.board.keys()):
                self.board[coordinates] = [obj]
                continue

            self.board[obj.coords].append(obj)

    def remove_from_board(self, objects, coordinate):
        if type(objects) is not list:
            objects = [objects]

        for obj in objects:
            if coordinate not in list(self.board.keys()):
                return

            self.board[coordinate].remove(obj)

            if len(self.board[coordinate]) == 0:
                self.board[coordinate] = []

    def move_ship(self, ship, translation):
        new_coordinates = (ship.coords[0] + translation[0], ship.coords[1] + translation[1])
        old_coordinates = ship.coords

        if new_coordinates != ship.coords:
            self.remove_from_board(ship, ship.coords)
            ship.update_coordinates(new_coordinates)
            self.add_to_board(ship, new_coordinates)

        self.logs.write('\tMoving player ' + str(ship.player_num) + ' ' + str(ship.name) + ' ' + str(ship.ship_num) + ': ' + str(old_coordinates) + ' -> '+ str(new_coordinates) + '\n')

    def get_ship_obj(self, ship_name, player_number, coordinates, ship_num):
        if ship_name == 'Scout':
            return Scout(player_number, coordinates, ship_num)

        if ship_name == 'BattleCruiser':
            return BattleCruiser(player_number, coordinates, ship_num)

        if ship_name == 'Battleship':
            return Battleship(player_number, coordinates, ship_num)

        if ship_name == 'Cruiser':
            return Cruiser(player_number, coordinates, ship_num)

        if ship_name == 'Destroyer':
            return Destroyer(player_number, coordinates, ship_num)

        if ship_name == 'Dreadnaught':
            return Dreadnaught(player_number, coordinates, ship_num)

    def initialize_game(self):
        starting_coordinates = [(mid_y - 1, 0), (mid_y - 1, board_x - 1), (0, mid_x - 1), (board_y - 1, mid_x - 1)]

        self.logs.write(str(len(self.players)) + ' Players are playing\n')
        self.logs.write('INITIALIZING GAME...\n\n')

        for n in range(len(self.players)):
            player = self.players[n]
            player.strategy.turn = self.turn
            player_number = self.players[n].player_num
            coordinates = starting_coordinates[n]
            player.set_home_colony(coordinates)
            self.add_to_board(player.home_colony, coordinates)
            self.logs.write('Player ' + str(player_number) + ' starting at ' + str(coordinates) + '\n')

            initial_ships = player.buy_ships(self.initial_cp)
            total_cp = 0
            ships = []

            for ship_name in initial_ships:
                for n in range(initial_ships[ship_name]):
                    ship = self.get_ship_obj(ship_name, player_number, coordinates, n + 1)
                    ships.append(ship)
                    total_cp += ship.cp_cost

            if total_cp <= self.initial_cp:
                for ship in ships:
                    player.add_ship(ship)
                    player.ship_counter[ship.name] += 1
                    self.add_to_board(ship, coordinates)

                player.cp = player.cp - total_cp

            else: 
                self.logs.write('Went over CP budget, no ships given\n')

        self.turn = 1
        self.logs.write('\n')

    def get_simple_board(self):
        simple_board = {key: [obj.__dict__ for obj in self.board[key]] for key in self.board if len(self.board[key]) != 0}

        for player in self.players:
            player.strategy.simple_board = simple_board
            player.strategy.turn = self.turn

    def confirm_hit(self, attacker, defender):
        if attacker.hp <= 0 or defender.hp <= 0:
            self.logs.write('Attempted combat with dead ship stopped\n')
            return None

        if attacker.player_num == defender.player_num:
            self.logs.write('Attemped combat with own ship stopped\n')
            return None

        roll = random.randint(1, 10)
        new_atk = attacker.atk - defender.df
        self.logs.write('\Player ' + str(attacker.player_num) + ' ' + str(attacker.name)+' ' + str(attacker.ship_num) + ' attacking player '+str(defender.player_num)+' '+str(defender.name) + ' ' + str(defender.ship_num) + '...')

        if roll <= new_atk or roll == 1:
            self.logs.write('Hit!\n')
            return True

        self.logs.write('Miss\n')
        return False

    def remove_ship(self, ship):
        player = self.players[ship.player_num - 1]
        player.ships.remove(ship)
        self.remove_from_board(ship, ship.coords)

    def complete_movement_phase(self):
        if self.winner != None:
            return

        self.logs.write('Start turn ' + str(self.turn) + ' Movement phase\n\n')

        for player in self.players:
              if len(player.ships) == 0:
                  self.logs.write('PLAYER ' + str(player.player_num) + ' HAS NO SHIPS\n\n')
                  continue

              self.logs.write('PLAYER ' + str(player.player_num) + ' MOVING:\n')
  
              for ship in player.ships:
                if self.is_enemy_in_translation(ship):
                    continue

                options = self.get_in_bounds_translations(ship.__dict__['coords'])
                move = player.choose_translation(ship.__dict__, options)

                if move not in options:
                    self.logs.write('\tIllegal move\n')
                    continue

                self.move_ship(ship, move)
                self.is_enemy_in_translation(ship)
                self.get_simple_board()

              self.logs.write('\n')

        self.logs.write('End turn ' + str(self.turn) + ' movement phase\n\n')

    def dict_to_obj(self, input_dict):
        for item in self.board[input_dict['coords']]:
            if item.__dict__ == input_dict:
                return item

    def get_all_ships(self, coordinate):
        return [obj for obj in self.board[coordinate] if isinstance(obj, Ship)]

    def get_ship_num(self, player, ship_name):
        for key in player.ship_counter:
            if key == ship_name:
                return player.ship_counter[key] + 1

    def check_buy_ships(self, player):
        wanted_ships = player.buy_ships(player.cp)

        if wanted_ships == None:
            return player.cp

        total_cp = 0
        ships = []

        for ship_name in wanted_ships:
            for n in range(wanted_ships[ship_name]):
                ship_num = self.get_ship_num(player, ship_name)
                ship = self.get_ship_obj(ship_name, player.player_num, player.home_colony.coords, ship_num)
                ships.append(ship)
                total_cp += ship.cp_cost

        if total_cp <= player.cp:
            for ship in ships:
                player.add_ship(ship)
                player.ship_counter[ship.name] += 1
                self.add_to_board(ship, player.home_colony.coords)
                self.logs.write('\nPlayer ' + str(player.player_num) + ' has bought a ' + str(ship.name))

            player.cp = player.cp - total_cp
            
        return player.cp

    def complete_economic_phase(self):
        if self.winner != None:
            return

        self.logs.write('Start turn ' + str(self.turn) + ' Economic phase\n')

        for player in self.players:
            player.cp += 10 * (len(player.colonies) + 1)

            player_ships = sorted(player.ships, reverse=True, key=lambda x: x.maint_cost)
            total_maint_cost = 0

            for ship in player_ships:
                total_maint_cost += ship.maint_cost

            if (player.cp - total_maint_cost) >= 0:
                player.cp -= total_maint_cost

            else:
                while player.cp - total_maint_cost < 0:
                    delete_ship = player_ships.pop()
                    total_maint_cost -= delete_ship.maint_cost                   
                    self.logs.write('\nPlayer ' + str(player.player_num) + ' ' + str(delete_ship.name) + ' ' + str(delete_ship.ship_num) + ' has been deleted')
                    self.remove_ship(delete_ship)

            self.check_buy_ships(player)
            self.logs.write('\nPlayer ' + str(player.player_num) + ' has ' + str(player.cp) + ' cp left\n')

        self.logs.write('\nEnd turn ' + str(self.turn) + ' Economic phase\n\n')
        self.turn += 1

    def complete_combat_phase(self):
        if self.winner != None:
            return

        self.logs.write('Beginning of turn ' + str(self.turn) + ' combat phase\n\n')

        dead_ship_coordinates = []

        for coordinate in self.combat_coordinates:
            sorting = sorted(self.get_all_ships(coordinate), key=lambda x: x.ship_class)

            while len(set([obj.player_num for obj in self.board[coordinate] if obj.obj_type != 'Colony'])) != 1 and len(sorting) > 0:
                self.logs.write('Combat at ' + str(coordinate) + ':\n\n')
                self.logs.write('Combat order:\n')

                for ship in sorting:
                    self.logs.write('\tPlayer ' + str(ship.player_num) + ' ' + str(ship.name) + ' ' + str(ship.ship_num) + '\n\n')

                for ship in sorting:
                    if ship.hp <= 0:
                        continue

                    player = self.players[ship.player_num - 1]
                    opponents = [thing for thing in sorting if thing.player_num != ship.player_num and thing.hp > 0]

                    if len(opponents) == 0:
                        continue

                    target_info = player.choose_target(ship.__dict__, [ship.__dict__ for ship in sorting])
                    target = self.dict_to_obj(target_info)

                    if target not in opponents:
                        self.logs.write('Invalid target\n')
                        continue

                    if self.confirm_hit(ship, target):
                        target.hp -= 1

                        if target.hp <= 0:
                            self.logs.write('\Player ' + str(target.player_num) + ' ' + str(target.name) + ' ' + str(target.ship_num)+' was destroyed in combat\n')
                            self.remove_ship(target)

                    self.get_simple_board()

                for ship in sorting:
                    if ship.hp <= 0:
                        sorting.remove(ship)

                if len(set([ship.player_num for ship in sorting])) == 1 or len(sorting) == 0:
                    dead_ship_coordinates.append(coordinate)

                self.logs.write('\n')

            for coordinate in dead_ship_coordinates:
                self.combat_coordinates.remove(coordinate)

        self.logs.write('End turn ' + str(self.turn) + ' combat phase\n\n')

    def remove_player(self, player):
        for ship in player.ships:
            self.remove_ship(ship)

        for colony in player.colonies:
            self.remove_from_board(colony, colony.coords)

        self.players.remove(player)
        self.remove_from_board(player.home_colony, player.home_colony.coords)

    def is_enemy_in_my_home_colony(self, home_colony):
        for obj in self.board[home_colony.coords]:
            if obj.player_num != home_colony.player_num:
                return True

        return False

    def check_for_winner(self):
        for player in self.players:
            if self.is_enemy_in_my_home_colony(player.home_colony):
            #if self.is_enemy_in_translation(player.home_colony):
                self.logs.write('Player '+str(player.player_num)+' was removed from the game\n\n')
                self.remove_player(player)

        if len(self.players) == 1:
            self.winner = self.players[0].player_num
            self.logs.write('Player ' + str(self.winner)+' won')

        if len(self.players) == 0:
            self.logs.write('Tie')
            self.winner = "Tie"

        if self.turn > self.max_turns:
            self.logs.write("Tie")
            self.winner = "Tie"

    def run_to_completion(self):
        while self.winner == None:
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.complete_economic_phase()
            self.check_for_winner()
