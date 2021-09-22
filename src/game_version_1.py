import math
import sys
import inspect
import random
sys.path.append('src')
from logger import *
from ship import *
from colony import *


class Game:
    def __init__(self, players, board_size=[7,7]):
        self.logs = Logger('/home/runner/space-empires/logs/game_version_1.txt')
        self.logs.clear_log()
        self.players = players
        self.set_player_numbers()
        self.board_size = board_size
        self.combat_coordinates = []
 
        global board_x, board_y, mid_x, mid_y
        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2
 
        self.board = [[[] for _ in range(board_x)] for _ in range(board_y)]
        self.turn = 1
        self.winner = None
 
        self.set_game()

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
        for item in self.board[ship.coordinates[1]][ship.coordinates[0]]:
            if item.player_number != ship.player_number:
                if ship.coordinates not in self.combat_coordinates and isinstance(ship, Ship) and isinstance(item, Ship):
                    self.combat_coordinates.append(ship.coordinates)

                return True

        return False

    def add_to_board(self, objects, coordinates):
        self.board[coordinates[1]][coordinates[0]].append(objects)

    def remove_from_board(self, objects, coordinate):
        self.board[coordinate[1]][coordinate[0]].remove(objects)
    
    def move_ship(self, ship, translation):
        new_coords = [ship.coordinates[n] + translation[n] for n in range(len(ship.coordinates))]

        self.logs.write('\tMOVING PLAYER '+str(ship.player_number)+' '+str(ship.name)+' '+str(ship.num)+': '+str(ship.coordinates)+' -> '+str(new_coords)+'\n')

        self.remove_from_board(ship, ship.coordinates)
        ship.update_coordinates(new_coords)
        self.add_to_board(ship, new_coords)

    def set_game(self):
        starting_coordinates = [(0, mid_x - 1), (board_y - 1, mid_x - 1), (mid_y - 1, 0), (mid_y - 1, board_x - 1)]

        self.logs.write(str(len(self.players)) + ' Players are playing\n')
        self.logs.write('INITIALIZING GAME...\n\n')
 
        for n in range(len(self.players)):
            player = self.players[n]
            player_number = self.players[n].player_number
            coordinates = starting_coordinates[n]
            player.set_home_colony(coordinates)
            self.add_to_board(player.home_colony, coordinates)
            self.logs.write('Player ' + str(player_number) + ' starting at ' + str(coordinates) + '\n')

            for n in range(3):
                scout = Scout(player_number, coordinates, n + 1)
                #battle_cruiser = BattleCruiser(player_number, coordinates, n + 1)
                self.add_to_board(scout, coordinates)
                #self.add_to_board(battle_cruiser, coordinates)

                player.add_ship(scout)
                #player.add_ship(battle_cruiser)

        self.logs.write('\n')

    def confirm_hit(self, attacker, defender):
        if attacker.hp <= 0 or defender.hp <= 0:
            self.logs.write('Attempted combat with dead ship stopped\n')
            return None

        if attacker.player_number == defender.player_number:
            self.logs.write('Attemped combat with own ship stopped\n')
            return None

        roll = random.randint(1, 10)
        new_atk = attacker.atk - defender.defense
        self.logs.write('\Player ' + str(attacker.player_number) + ' ' + str(attacker.name)+' ' + str(attacker.num) + ' attacking player '+str(defender.player_number)+' '+str(defender.name) + ' ' + str(defender.num) + '...')

        if roll <= new_atk:
            self.logs.write('Hit!\n')
            return True

        self.logs.write('Miss\n')
        return False

    def complete_movement_phase(self):
        if self.winner != None:
            return

        self.logs.write('Start turn ' + str(self.turn) + ' Movement phase\n\n')

        for player in self.players:
              if len(player.ships) == 0:
                  self.logs.write('PLAYER ' + str(player.player_number) + ' HAS NO SHIPS\n\n')
                  continue

              self.logs.write('PLAYER ' + str(player.player_number) + ' MOVING:\n')
              opponent_home_colony = [p.home_colony.coordinates for p in self.players if p.player_number != player.player_number]
  
              for ship in player.ships:
                  if self.is_enemy_in_translation(ship):
                      continue

                  options = self.get_in_bounds_translations(ship.coordinates)
                  translation = player.select_translation(ship.coordinates, options, opponent_home_colony)

                  if translation not in options:
                      self.logs.write('Invalid option\n')
                      continue


                  self.move_ship(ship, translation)
                  self.is_enemy_in_translation(ship)

              self.logs.write('\n')

        self.logs.write('End turn ' + str(self.turn) + ' movement phase\n\n')

    def complete_combat_phase(self):
        if self.winner != None:
            return

        self.logs.write('Beginning of turn ' + str(self.turn) + ' combat phase\n\n')

        dead_ship_coordinates = []

        for coordinate in self.combat_coordinates:
            self.logs.write('Combat at ' + str(coordinate) + ':\n\n')

            sorting = sorted([obj for obj in self.board[coordinate[1]][coordinate[0]] if isinstance(obj, Ship)], key=lambda x: x.ship_class)

            self.logs.write('\Combat Order:\n')

            for ship in sorting:
                self.logs.write('\t\Player ' + str(ship.player_number) + ' ' + str(ship.name) + ' ' + str(ship.num) + '\n')
                self.logs.write('\n\tStarting combat...\n\n')

            for ship in sorting:
                if ship.hp <= 0:
                    continue

                player = self.players[ship.player_number - 1]
                opponents = [thing for thing in sorting if thing.player_number != ship.player_number and thing.hp > 0]

                if len(opponents) == 0:
                    continue

                target = player.select_target(opponents)

                if target not in opponents:
                    self.logs.write('Invalid target\n')
                    continue

                if self.confirm_hit(ship, target):
                    target.hp -= 1

                    if target.hp <= 0:
                        self.logs.write('\Player ' + str(target.player_number) + ' ' + str(target.name) + ' ' + str(target.num)+' was destroyed in combat\n')
                        player = self.players[ship.player_number - 1]
                        player.ships.remove(ship)
                        self.remove_from_board(ship, ship.coordinates)

            for ship in sorting:
                if ship.hp <= 0:
                    sorting.remove(ship)

            if len(set([ship.player_number for ship in sorting])) == 1 or len(sorting) == 0:
                dead_ship_coordinates.append(coordinate)

            self.logs.write('\n')

        for coordinate in dead_ship_coordinates:
            self.combat_coordinates.remove(coordinate)

        self.logs.write('End turn ' + str(self.turn) + ' combat phase\n\n')
        self.turn += 1

    def remove_player(self, player):
        for ship in player.ships:
            player = self.players[ship.player_number - 1]
            player.ships.remove(ship)
            self.remove_from_board(ship, ship.coordinates)

        for colony in player.colonies:
            self.remove_from_board(colony, colony.coordinates)

        self.players.remove(player)
        self.remove_from_board(player.home_colony, player.home_colony.coordinates)

    def check_for_winner(self):
        for player in self.players:
            if self.is_enemy_in_translation(player.home_colony):
                self.logs.write('Player '+str(player.player_number)+' was removed from the game\n\n')
                self.remove_player(player)

        if len(self.players) == 1:
            self.winner = self.players[0].player_number
            self.logs.write('Player ' + str(self.winner)+' won')

        if len(self.players) == 0:
            self.logs.write('Tie')
            self.winner = "Tie"

    def run_to_completion(self):
        while self.winner == None:
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.check_for_winner()