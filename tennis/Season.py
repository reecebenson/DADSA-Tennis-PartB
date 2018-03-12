"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Tournament

class Season():
    # Variables
    name = None
    game = None
    json_data = None
    tournaments = { }
    players = { }

    def __init__(self, _game, _name, _json_data):
        self.name = _name
        self.game = _game
        self.json_data = _json_data

        # Read in Tournament Data
        for tournament in _json_data["tournaments"]:
            tournament_data = _json_data["tournaments"][tournament]

            # Load our Tournament in (if it is new)
            if(tournament not in self.tournaments):
                # Create our Tournament Object
                self.tournaments.update({ tournament: Tournament.Tournament(self.game, tournament, tournament_data) })

        if(_game.debug):
            print("[SEASON]: Season '{}' made!".format(_name))