"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Match

class Round():
    # Variables
    id = None
    name = None
    game = None
    json_data = None
    matches = { }

    def __init__(self, _game, _name, _json_data):
        self.name = _name
        self.id = int(_name[-1:])
        self.game = _game
        self.json_data = _json_data

        # Read in Gender Round Data
        for gender in _json_data:
            gender_data = _json_data[gender]
            print(gender)

            # Add Gender to Matches
            if(gender not in self.matches):
                self.matches.update({ gender: [ ] })

            # Read in Round
            for match in gender_data:
                # Add our Match to the Round Gender
                self.matches[gender].append(Match.Match())

        if(_game.debug):
            print("[ROUND]: Round '{}' made!".format(self.id))