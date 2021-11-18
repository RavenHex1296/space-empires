class Ship:
    def __init__(self):
        self.obj_type = 'Ship'

    def update_coordinates(self, new_coordinates):
        self.coords = new_coordinates


class Scout(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 1
        self.atk = 3
        self.df = 0
        self.name = 'Scout'
        self.player_num = player_number
        self.ship_class = "E"
        self.coords = coordinates
        self.ship_num = num
        self.cp_cost = 6
        Ship.__init__(self)


class BattleCruiser(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 2
        self.atk = 5
        self.df = 1
        self.name = 'BattleCruiser'
        self.player_num = player_number
        self.ship_class = "B"
        self.coords = coordinates
        self.ship_num = num
        self.cp_cost = 15
        Ship.__init__(self)


class BattleShip(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 3
        self.atk = 5
        self.df = 2
        self.name = 'BattleShip'
        self.player_num = player_number
        self.ship_class = "A"
        self.coords = coordinates
        self.ship_num = num
        self.cp_cost = 20
        Ship.__init__(self)

class Cruiser(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 2
        self.atk = 4
        self.df = 1
        self.name = 'Cruiser'
        self.player_num = player_number
        self.ship_class = "C"
        self.coords = coordinates
        self.ship_num = num
        self.cp_cost = 12
        Ship.__init__(self)


class Destroyer(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 1
        self.atk = 4
        self.df = 0
        self.name = 'Destroyer'
        self.player_num = player_number
        self.ship_class = "D"
        self.coords = coordinates
        self.ship_num = num
        self.cp_cost = 9
        Ship.__init__(self)


class Dreadnaught(Ship):
    def __init__(self, player_number, coordinates, num=None):
        self.hp = 3
        self.atk = 6
        self.df = 3
        self.name = 'Dreadnaught'
        self.player_num = player_number
        self.ship_class = "A"
        self.coords = coordinates
        self.ship_num = num
        self.cp_cost = 24
        Ship.__init__(self)
