class Ship:
    def update_coordinates(self, new_coordinates):
        self.coordinates = new_coordinates

class Scout(Ship):
    def __init__(self, player_num, coordinates):
        self.hp = 1
        self.atk = 3
        self.defense = 0
        self.player_num = player_num
        self.ship_class = "E"
        self.coordinates = coordinates


class BattleCruiser(Ship):
    def __init__(self, player_num, coordinates):
        self.hp = 2
        self.atk = 5
        self.defense = 1
        self.player_num = player_num
        self.ship_class = "B"
        self.coordinates = coordinates

#general ship class, make board compatible, general colony class