import sys
sys.path.append('src/game_level_0_0')
from game import *
from player import *
from random_player import *
from custom_player import *


players = [RandomPlayer(), CustomPlayer()]
game = Game(players)

assert game.game_state == {
    'turn': 1,
    'board_size': [7,7],
    'players': {
        1: {
            'scout_coords': (4, 1),
            'home_colony_coords': (4, 1)
        },
        2: {
            'scout_coords': (4, 7),
            'home_colony_coords': (4, 7)
        }
    },
    'winner': None
}

game.complete_turn()
print(game.game_state, "\n")

game.run_to_completion()
print(game.game_state)
