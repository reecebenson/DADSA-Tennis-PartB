"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
import json
from tennis import Tournament
from tennis.File import File

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

        for t in season_data["tournaments"]:
            tournament = season_data["tournaments"][t]
            for r in tournament:
                if(r != "rounds"):
                    continue

                rounds = tournament["rounds"]
                for _r in rounds:
                    _round = rounds[_r]
                    _round_id = int(_r[-1:])
                    for gender in _round:
                        _matches = [ ]
                        #print(t, r, _round_id, gender)
                        _count = 0
                        for m in _round[gender]:
                            _matches.append(self.get_tournament(t).get_round(_round_id).get_matches(gender)[_count].get_match_as_json())
                            _count += 1
                        season_data["tournaments"][t]["rounds"]["round_{0}".format(_round_id)][gender] = _matches

        # Save
        return File().update_season(self.get_name(), season_data)