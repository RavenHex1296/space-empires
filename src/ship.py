class Ship:
    def __init__(self):
        self.obj_type = 'Ship'

    def update_coordinates(self, new_coordinates):
        self.coordinates = new_coordinates


class Scout(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.name = 'Scout'
        self.player_number = player_number
        self.ship_class = "E"
        self.coordinates = coordinates
        self.num = num
        Ship.__init__(self)


class BattleCruiser(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 2
        self.atk = 5
        self.df = 1
        self.name = 'BattleCruiser'
        self.player_number = player_number
        self.ship_class = "B"
        self.coordinates = coordinates
        self.num = num
        Ship.__init__(self)
