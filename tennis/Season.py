"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
import json
from tennis import Tournament
from tennis import File

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
                self.tournaments.update({ tournament: Tournament.Tournament(self.game, tournament, self, tournament_data) })
            else:
                print("Something is fucked!")

        if(_game.debug):
            print("[SEASON]: Season '{}' made!".format(_name))

        self.validate_season()

    def get_name(self):
        return self.name

    def get_tournaments(self):
        return [ self.tournaments[t] for t in self.tournaments ]

    def get_tournament(self, tournament_name):
        return self.tournaments[tournament_name]

    def validate_season(self):
        # Validate Tournaments
        for t in self.get_tournaments():
            # Check Round Size
            if(len(t.get_rounds()) is not self.game.settings['round_count']):
                self.game.clear_screen()
                print("The Round Count of {0}, {1} is invalid! Round Limit: {2}, Round Count: {3}".format(self.get_name(), t.get_name(), self.game.settings['round_count'], len(t.get_rounds())))
                exit()
            
            # Validate Rounds
            for r in t.get_rounds():
                for g in r.get_genders():
                    # Validate Matches
                    for m in r.get_matches(g):
                        m.validate_match(self.game.settings['score_limit'][g], r.get_id())

            # Save Data
            self.save()

    def save(self):
        # Grab all data
        season_data = self.json_data

        c = 0
        for m in season_data["tournaments"]["TAC1"]["rounds"]["round_3"]["male"]:
            print(m, "---", self.get_tournament("TAC1").get_round(3).get_matches("male")[c].get_match_as_json())
            c += 1
        #print(season_data["tournaments"]["TAC1"]["rounds"]["round_1"]["male"][0])

        #print(json.dumps(season_data, indent=4, sort_keys=True))

        # Save
        #return File.update(season, season_data)