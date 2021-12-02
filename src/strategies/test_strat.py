'''
    def choose_translation(self, ship_info, possible_translations):
        opponent_home_colony = []

        for key in self.simple_board:
            for obj in self.simple_board[key]:
                if obj['obj_type'] == 'Colony' and obj['player_num'] != ship_info['player_num'] and obj['is_home_colony'] == True:
                    opponent_home_colony.append(key)

        closest_colony = self.best_option(opponent_home_colony, ship_info['coords'])
        best_translation = self.best_translation(possible_translations, ship_info['coords'], closest_colony)

        if ship_info['name'] == 'Scout' and self.is_enemy_in_translation(ship_info, best_translation):
            other_translations = [translation for translation in possible_translations if translation != best_translation and translation != (0, 0)]
            return self.get_next_best_translation(ship_info, other_translations, opponent_home_colony[0])

        if self.is_enemy_in_translation(ship_info, best_translation):
            return (0, 0)

        return best_translation

    def choose_translation(self, ship_info, possible_translations):
        opponent_home_colony = []
        my_home_colony_coords = None

        for key in self.simple_board:
            for obj in self.simple_board[key]:
                if obj['obj_type'] == 'Colony' and obj['player_num'] != ship_info['player_num'] and obj['is_home_colony'] == True:
                    opponent_home_colony.append(key)

                if obj['obj_type'] == 'Colony' and obj['player_num'] == ship_info['player_num'] and obj['is_home_colony'] == True:
                    my_home_colony_coords = key

        closest_colony = self.best_option(opponent_home_colony, ship_info['coords'])
        best_translation = self.best_translation(possible_translations, ship_info['coords'], closest_colony)

        if not self.enemy_ships_left(ship_info['player_num']):
            return best_translation

        if ship_info['name'] == 'Scout' and self.is_enemy_in_translation(ship_info, best_translation):
            other_translations = [translation for translation in possible_translations if translation != best_translation and translation != (0, 0)]
            return self.get_next_best_translation(ship_info, other_translations, opponent_home_colony[0])

        if ship_info['name'] == 'Scout' and not self.is_enemy_in_translation(ship_info, best_translation):
            return best_translation

        if ship_info['name'] == 'Dreadnaught' and self.enemy_ships_left(ship_info['player_num']):
            defense_coordinates = self.get_around_colony_coordinates(my_home_colony_coords, ship_info['player_num'])
            priority_coordinate = defense_coordinates[-1]
            defense_coordinates.pop()

            for coordinate in defense_coordinates:
                if not self.are_my_ships_in_coord(coordinate, ship_info['player_num']):
                    return self.get_optimal_translation(ship_info, possible_translations, coordinate)

                if self.are_my_ships_in_coord(coordinate, ship_info['player_num']):
                    if ship_info['coords'] == coordinate:
                        return (0, 0)

            return self.get_optimal_translation(ship_info, possible_translations, priority_coordinate)
'''