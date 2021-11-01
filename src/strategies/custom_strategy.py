import math, random

class CustomStrategy():
    def __init__(self):
        self.simple_board = None

    def choose_translation(self, ship_info, possible_translations):

    def get_enemies(self, own_ship, combat_order):
        player_num = own_ship['player_num']
        enemies = []

        for ship_info in combat_order:
            if ship_info['player_num'] != player_num and ship_info['hp'] > 0:
                enemies.append(ship_info)
        return enemies
    
    def choose_target(self, ship_info, combat_order):
        enemies = self.get_enemies(ship_info, combat_order)
        optimal_enemies = []

        for enemy in enemies:
            if enemy['ship_class'] >= ship_info['ship_class'] and ship_info['hp'] >= enemy['hp']:
                optimal_enemies.append(enemy)

        if len(optimal_enemies) != 0:
            random.choice(optimal_enemies)

        else:
            random.choice(enemies)