import sys
sys.path.append('src')
from ship import *

scout = {'hp': 1, 'atk': 3, 'df': 0, 'name': 'Scout', 'ship_class': 'E', 'cp_cost': 6, 'obj': Scout}
battlecruiser = {'hp': 2, 'atk': 5, 'df': 1, 'name': 'BattleCruiser', 'ship_class': 'B', 'cp_cost': 15, 'obj': BattleCruiser}
battleship = {'hp': 3, 'atk': 5, 'df': 2, 'name': 'Battleship', 'ship_class': 'A', 'cp_cost': 20, 'obj': Battleship}
cruiser = {'hp': 2, 'atk': 4, 'df': 1, 'name': 'Cruiser', 'ship_class': 'C', 'cp_cost': 12, 'obj': Cruiser}
destroyer = {'hp': 1, 'atk': 4, 'df': 0, 'name': 'Destroyer', 'ship_class': 'D', 'cp_cost': 9, 'obj': Destroyer}
dreadnaught = {'hp': 3, 'atk': 6, 'df': 3, 'name': 'Dreadnaught', 'ship_class': 'A', 'cp_cost': 24, 'obj': Dreadnaught}
