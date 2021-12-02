import sys
sys.path.append('src')
from game import *
sys.path.append('src/strategies')
from test_strategy import *
from illegal_strategy import *
from me import *
from maia import *
from charlie import *
from custom_strategy import *
from justin import *
from william import *
from anton import *
from logger import *
from player import *
from ship import *
sys.path.append('src/old stuff')
from custom_player import *
from pause_strategy import *
import time

'''
players = [Player(IllegalStrategy()), Player(IllegalStrategy())]
game = Game(players)


for _ in range(5):
    game.complete_movement_phase()
    game.complete_combat_phase()

initial_coordinates = players[0].ships[0].coordinates

game.complete_movement_phase()
game.complete_combat_phase()

assert players[0].ships[0].coordinates == initial_coordinates
print("PASSED")


players = [Player(CustomStrategy()), Player(PauseStrategy())]
game = Game(players)


for _ in range(3):
    game.complete_movement_phase()
    game.complete_combat_phase()

game.complete_movement_phase()


combat_coordinates = game.combat_coordinates[0]

all_objects = game.board[combat_coordinates[1]][combat_coordinates[0]]

all_ships = [thing for thing in all_objects if isinstance(thing, Ship)]


assert all_ships[0].player_number == 1
print('PASSED')



players = [Player(CustomStrategy()), Player(IllegalStrategy())]
game = Game(players)
game.run_to_completion()

assert game.winner == 1
print("PASSED")

players = [Player(MoveToEnemyHomeColony()), Player(Custom())]
game = Game(players)
game.run_to_completion()
print("Me vs William:", game.winner)

players = [Player(MoveToEnemyHomeColony()), Player(StraightToEnemyColony())]
game = Game(players)
game.run_to_completion()
print("Me vs Maia:", game.winner)

players = [Player(MoveToClosestCol()), Player(MoveToEnemyHomeColony())]
game = Game(players)
game.run_to_completion()
print("Justin vs me:", game.winner)

players = [Player(MoveToOpponent()), Player(MoveToEnemyHomeColony())]
game = Game(players)
game.run_to_completion()
print("Charlie vs me:", game.winner)
'''


def simulate_me_vs_other(num_games):
    win_data = {1: 0, 2: 0, "Tie": 0}

    for _ in range(num_games):
        players = [Player(CaydenStrat()), Player(TestStrategy())]
        game = Game(players)
        game.run_to_completion()

        win_data[game.winner] += 1

    return win_data[1] / (win_data[1] + win_data[2] + win_data['Tie'])

def simulateother_vs_me(num_games):
    win_data = {1: 0, 2: 0, "Tie": 0}

    for _ in range(num_games):
        players = [Player(TestStrategy()), Player(CaydenStrat())]
        game = Game(players)
        game.run_to_completion()

        win_data[game.winner] += 1

    return win_data[2] / (win_data[1] + win_data[2] + win_data['Tie'])


print("Me vs Other:", simulate_me_vs_other(1000), '\n', 'Other vs Me:', simulateother_vs_me(1000))
