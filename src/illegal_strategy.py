from random import random
import math
import sys
sys.path.append('src')
from ship import *
from colony import *

class IllegalStrategy():
    def select_translation(self, coordinates, options, desired_location):
        return (0, 1)

    def select_target(self, options):
        return enemies[random.randint(0, len(enemies) - 1)]