import math
import random
#will fix later but made me mald so hard atm
class CustomStrategy():
    def select_translation(self, ship_coords, choices, opp_home_cols):
        return (1, 0)

    def select_target(self, enemies):
        if len(enemies)==1:
            return enemies[0]

        return enemies[random.randint(0, len(enemies)-1)]