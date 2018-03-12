"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Round

class Tournament():
    # Variables
    name = None
    game = None
    json_data = None
    rounds = { }

    def __init__(self, _game, _name, _json_data):
        self.name = _name
        self.game = _game
        self.json_data = _json_data

        # Read in Round Data
        for round_number in _json_data["rounds"]:
            round_data = _json_data["rounds"][round_number]
            
            # Load our Round in (if it is new)
            if(round_number not in self.rounds):
                # Create our Tournament Object
                self.rounds.update({ round_number: Round.Round(self.game, round_number, round_data) })

        if(_game.debug):
            print("[TOURNAMENT]: Tournament '{}' made!".format(_name))