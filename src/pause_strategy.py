import math

import random

class PauseStrategy():
    def __init__(self):
        self.counter = 0

    def select_translation(self, ship_coords, choices, opp_home_cols):
        if self.counter < 7:
            self.counter += 1
            return (0, 0)
        
        else:
            return (-1, 0)

    def select_target(self, enemies):
        if len(enemies)==1:
            return enemies[0]

        return enemies[random.randint(0, len(enemies)-1)]