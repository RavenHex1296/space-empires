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
        self.home_colony.obj_type = 'HomeColony'

    def add_colonies(self, colonies):
        for colony in colonies:
            self.colonies.append(colony)

    def set_player_number(self, n):
        self.player_number = n

    def select_translation(self, ship_info, options):
        return self.strategy.select_translation(ship_info,options)
    
    def select_target(self, ship_info, combat_order):
        return self.strategy.select_target(ship_info, combat_order)
