import math
import sys
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
        if coordinates == None:
            return False

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
        for thing in self.board[ship.coordinates[1]][ship.coordinates[0]]:
            if thing.player_number != ship.player_number:
                return True

        return False

    def add_to_board(self, objects, coordinate):
        self.board[coordinate[1]][coordinate[0]].append(objects)

    def remove_from_board(self, objects, coordinate):
        self.board[coordinate[1]][coordinate[0]].remove(objects)
    
    def move_ship(self, ship, translation):
        x, y = ship.coordinates
        updated_coordinates = (x + translation[0], y + translation[1])
        self.board[x][y].remove(ship)
        self.board[updated_coordinates[0]][updated_coordinates[1]].append(ship)
        ship.coordinates = updated_coordinates

    def set_game(self):
        starting_coordinates = [(0, mid_x - 1), (board_y - 1, mid_x - 1), (mid_y - 1, 0), (mid_y - 1, board_x - 1)]
 
        for n in range(len(self.players)):
            player = self.players[n]
            player_number = self.players[n].player_number
            player.set_home_colony(starting_coordinates[n])
            self.add_to_board(player.home_colony, starting_coordinates[n])

            for num in range(3):
                scout = Scout(player_number, starting_coordinates[n])
                battle_cruiser = BattleCruiser(player_number, starting_coordinates[n])
                self.add_to_board(scout, starting_coordinates[n])
                self.add_to_board(battle_cruiser, starting_coordinates[n])

                player.add_ship(scout)
                player.add_ship(battle_cruiser)

    def get_combat_coordinates(self):
        combat_coordinates = []

        for y in range(board_y):
            for x in range(board_x):
                if len(self.board[y][x]) > 1:
                    for thing in self.board[y][x]:
                        if thing.player_number != self.board[y][x][0].player_number:
                              combat_locations.append((x, y))
                              break

        return combat_locations
    
    def get_ships_on_coordinate(self, player_number, coordinate):
        ships_on_coordinate = []

        for ship in self.board[coordinate[1]][coordinate[0]]:
            if ship.player_number == player_number:
                ships_on_coordinate.append[ship]

        return ships_on_coordinate 

    def complete_movement_phase(self):
        for player in self.players:
              for ship in player.ships:
                  if self.is_enemy_in_translation:
                      continue

                  options = self.get_in_bounds_translations(ship.coordinates)
                  translation = player.select_translation(ship.coordinates, options, [other_player.home_colony.coordinates for other_player in self.players if other_player.player_number != player.player_number])
                  self.move_ship(ship, translation)
                  self.add_to_board(ship, updated_coordinates)
                  ship.update_coordinates(updated_coordinates)
                  self.remove_from_board(ship, coordinates)
'''
    def complete_combat_phase(self):
        

    def run_to_completion(self):
        while self.winner == None:
            self.complete_movement_phase()
            self.complete_combat_phase()
'''