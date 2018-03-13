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
    tournaments = None
    players = None

    def __init__(self, _game, _name, _json_data):
        self.name = _name
        self.game = _game
        self.json_data = _json_data
        self.tournaments = { }
        self.players = { }

        # Read in Tournament Data
        for tournament in _json_data["tournaments"]:
            tournament_data = _json_data["tournaments"][tournament]

            # Load our Tournament in (if it is new)
            if(tournament not in self.tournaments):
                # Create our Tournament Object
                self.tournaments.update({ tournament: Tournament.Tournament(self.game, tournament, tournament_data) })
            else:
                print("Something is fucked!")

        if(_game.debug):
            print("[SEASON]: Season '{}' made!".format(_name))

        self.doSomething()

    def get_name(self):
        return self.name

    def get_tournaments(self):
        return [ self.tournaments[t] for t in self.tournaments ]

    def doSomething(self):
        for t in self.get_tournaments():
            for r in t.get_rounds():
                for m in r.get_matches("male"):
                    print(t.get_name(), r.get_name(), m.get_match_text())