import sys
sys.path.append('src')
from game_version_1 import *
from custom_player import *
from logger import *
from ship import *

players = [CustomPlayer(), CustomPlayer()]
game = Game(players)


game.complete_movement_phase()