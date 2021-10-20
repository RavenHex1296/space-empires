import sys
sys.path.append('src')
import random
from colony import *
from ship import *


class Player():
    def __init__(self, strategy):
        self.player_num = None
        self.ships = []
        self.home_colony = None
        self.colonies = []
        self.strategy = strategy

    def add_ship(self, ship):
        self.ships.append(ship)

    def set_home_colony(self, coordinates):
        self.home_colony = Colony(self.player_num, coordinates)
        self.home_colony.is_home_colony = True

    def add_colonies(self, colonies):
        for colony in colonies:
            self.colonies.append(colony)

    def set_player_number(self, n):
        self.player_num = n

    def choose_translation(self, ship_info, options):
        return self.strategy.choose_translation(ship_info, options)
    
    def choose_target(self, ship_info, combat_order):
        return self.strategy.choose_target(ship_info, combat_order)['ship_num']
