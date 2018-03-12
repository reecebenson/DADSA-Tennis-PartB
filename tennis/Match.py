"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""

class Match():
    # Variables
    id = None
    name = None
    game = None
    json_data = None
    gender = None
    player_one = None
    player_two = None
    player_one_score = None
    player_two_score = None

    def __init__(self, _game, _name, _json_data):
        self.name = _name
        self.id = int(_name[-1:])
        self.game = _game
        self.json_data = _json_data

        if(_game.debug):
            print("[ROUND]: Round '{}' made!".format(self.id))