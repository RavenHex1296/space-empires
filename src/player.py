import sys
sys.path.append('src')
import random
from colony import *
from ship import *


class Player():
    def __init__(self, strategy):
        self.player_number = None
        self.ships = []
        self.home_colony = None
        self.colonies = []
        self.strategy = strategy

    def add_ship(self, ship):
        self.ships.append(ship)

    def set_home_colony(self, coordinates):
        self.home_colony = Colony(self.player_number, coordinates)

    def add_colonies(self, colonies):
        for colony in colonies:
            self.colonies.append(colony)

    def set_player_number(self, n):
        self.player_number = n

    def select_translation(self, coordinates, options, desired_location):
        return self.strategy.select_translation(coordinates, options, desired_location)

    def select_target(self, options):
        return self.strategy.select_target(options)
