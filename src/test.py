import sys
sys.path.append('src')
from game_version_1 import *
from illegal_strategy import *
from custom_strategy import *
from logger import *
from player import *
from ship import *
sys.path.append('src/old stuff')
from custom_player import *
from pause_strategy import *


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