"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Match
from tennis import MatchGender
from tennis.Menu import Menu
from tennis.Menu import Builder
from functools import partial

class Round():
    # Variables
    id = None
    name = None
    game = None
    parent = None
    json_data = None
    matches = None
    genders = None
    genders_available = None

    def __init__(self, _game, _name, _parent, _json_data):
        self.parent = _parent
        self.name = _name
        self.id = int(_name[-1:])
        self.game = _game
        self.json_data = _json_data
        self.genders = { }

        # Read in Gender Round Data
        for gender in _json_data:
            gender_data = _json_data[gender]

            # Create a Gender Match
            match_gender = MatchGender.MatchGender(_game, gender, self)
            match_gender.set_availability(True if self.id is 1 else False)
            self.genders.update({ gender: match_gender })

            # Read in Round
            if(self.parent.parent.get_id() == 1):
                for match in gender_data:
                    # Add our Match to the Round Gender
                    match_gender.add_match(match)

        if(_game.debug):
            print("[ROUND]: Round '{}' made!".format(self.id))

    def get_name(self):
        return self.name

    def get_gender(self, gender):
        return (gender, self.genders[gender]) if gender in self.genders else (None,None)

    def get_genders(self):
        return [ (g, self.genders[g]) for g in self.genders ]

    def get_id(self):
        return self.id