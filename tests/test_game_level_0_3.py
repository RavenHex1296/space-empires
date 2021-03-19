import sys
sys.path.append('src/game_level_0_3')
from game import *
from random_player import *
from custom_player import *

players = [CustomPlayer(), CustomPlayer()]
game = Game(players)
game.run_to_completion()
