import math
import random

class TestStrategy():
    def __init__(self, simple_board=None):
        self.simple_board = {}

    def copy_object(self, obj):
        copied_object = obj.__dict__

    def select_translation(self, ship_info, possible_translations):
        return None


'''
    def select_target(self, enemies):
        if len(enemies) == 1:
            return enemies[0]

        return enemies[random.randint(0, len(enemies)-1)]
'''