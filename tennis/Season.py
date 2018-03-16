"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
import json
from tennis.File import File
from tennis.Player import Player
from tennis import Tournament

class Season():
    # Variables
    name = None
    id = None
    game = None
    json_data = None
    tournaments = None
    players = None

    def __init__(self, _game, _name, _json_data, _players):
        self.name = _name
        self.id = _name[-1:]
        self.game = _game
        self.json_data = _json_data
        self.tournaments = { }
        self.players = { }
        self.genders = [ ]

        # Set our Players
        self.set_players(_players)

        # Read in Tournament Data
        for tournament in _json_data["tournaments"]:
            tournament_data = _json_data["tournaments"][tournament]

            # Load our Tournament in (if it is new)
            if(tournament not in self.tournaments):
                # Create our Tournament Object
                self.tournaments.update({ tournament: Tournament.Tournament(self.game, tournament, self, tournament_data) })

        if(_game.debug):
            print("[SEASON]: Season '{}' made!".format(_name))

        self.validate_season()

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_tournaments(self):
        return [ self.tournaments[t] for t in self.tournaments ]

    def get_tournament(self, tournament_name):
        return self.tournaments[tournament_name]

    def set_players(self, player_list):
        for gender in player_list[self.get_name()]:
            # Add Gender to Genders List
            if(gender not in self.genders):
                self.genders.append(gender)

            # Add Gender to Players List
            if(gender not in self.players):
                self.players.update({ gender: [ ] })

            # Create Player
            for player in player_list[self.get_name()][gender]:
                p = Player(player, gender, self)
                self.players[gender].append(p)
    
    def get_player(self, name, gender):
        if(gender in self.players):
            for player in self.players[gender]:
                if(player.get_name() == name):
                    return player
        return None

    def list_players(self):
        print("Season: {}\n".format(self.get_name()))
        for gender in self.players:
            print("Gender: {}, count: {}".format(gender, len(self.players[gender])))
            print("{0}\n".format(", ".join([ player.get_name() for player in self.players[gender] ])))

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
                    for m in g[1].get_matches():
                        m.validate_match(self.game.settings['score_limit'][g[1].get_gender()], r.get_id())

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
                        _count = 0
                        for m in _round[gender]:
                            _matches.append(self.get_tournament(t).get_round(_round_id).get_gender(gender)[1].get_matches()[_count].get_match_as_json())
                            _count += 1
                        season_data["tournaments"][t]["rounds"]["round_{0}".format(_round_id)][gender] = _matches

        # Save
        return File().update_season(self.get_name(), season_data)