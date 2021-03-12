import sys
sys.path.append('src/game_level_0_2')
from game import *
from random_player import *
from custom_player import *

num_wins = {1: 0, 2: 0}
scouts_remaining = {1: 0, 2: 0}
for _ in range(200):
    players = [CustomPlayer(), CustomPlayer()]
    game = Game(players)
    game.run_to_completion()
    winner = game.state['winner']
    scouts_remaining[winner] += len(game.state['players'][winner]['scout_coords'])

    num_wins[winner] += 1

avg_scouts_remaining = {k:v/200 for k,v in scouts_remaining.items()}

print(num_wins, "\n")
print(avg_scouts_remaining )
