import sys
sys.path.append('src/game_level_0_2_random_seeds')
from game import *
from random_player import *
from custom_player import *

tests = [
    {'seed': 0, 'winner': 2},
    {'seed': 1, 'winner': 1},
    {'seed': 2, 'winner': 2},
    {'seed': 3, 'winner': 1},
    {'seed': 4, 'winner': 1},
    {'seed': 5, 'winner': 2},
    {'seed': 6, 'winner': 2},
    {'seed': 7, 'winner': 1},
    {'seed': 8, 'winner': 1},
    {'seed': 9, 'winner': 1}
]
print("Testing...")
for test in tests:
    players = [CustomPlayer(), CustomPlayer()]
    random_seed = test['seed']

    game = Game(players, random_seed)
    game.run_to_completion()

    desired_winner = test['winner']
    assert(game.state['winner'] == desired_winner)
print("Success")
