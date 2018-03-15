"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Round

class Tournament():
    # Variables
    name = None
    game = None
    parent = None
    json_data = None
    rounds = None
    gender = None

    def __init__(self, _game, _name, _parent, _json_data):
        self.name = _name
        self.game = _game
        self.parent = _parent
        self.json_data = _json_data
        self.rounds = { }

        # Read in Round Data
        for round_number in _json_data["rounds"]:
            round_data = _json_data["rounds"][round_number]
            
            # Load our Round in (if it is new)
            if(round_number not in self.rounds):
                # Create our Tournament Object
                self.rounds.update({ round_number: Round.Round(self.game, round_number, self, round_data) })

        if(_game.debug):
            print("[TOURNAMENT]: Tournament '{}' made!".format(_name))

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_rounds(self):
        return [ self.rounds[r] for r in self.rounds ]

    def get_round(self, round_id):
        return self.rounds["round_{0}".format(round_id)]
