"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Match
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
        self.matches = { }
        self.genders = [ ]
        self.genders_available = { }

        # Read in Gender Round Data
        for gender in _json_data:
            gender_data = _json_data[gender]

            # Add Gender to Matches
            if(gender not in self.matches):
                self.genders.append(gender)
                self.matches.update({ gender: [ ] })
                self.genders_available.update({ gender: True if self.id is 1 else False })

            # Read in Round
            for match in gender_data:
                # Add our Match to the Round Gender
                self.matches[gender].append(Match.Match(_game, gender, self, match))

        if(_game.debug):
            print("[ROUND]: Round '{}' made!".format(self.id))

    def get_name(self):
        return self.name

    def get_genders(self):
        return self.genders

    def get_id(self):
        return self.id

    def get_matches(self, gender):
        if(gender in self.matches):
            return [ m for m in self.matches[gender] ]
        else:
            return [ ]

    def get_players(self, gender):
        players = [ ]
        for m in self.get_matches(gender):
            players.append(m.player_one)
            players.append(m.player_two)
        return players

    def get_winners(self, gender):
        return [ m.get_winner() for m in self.get_matches(gender) ]

    def is_available(self, gender):
        return self.genders_available[gender]

    def set_available(self, gender):
        if(gender in self.genders_available):
            self.genders_available[gender] = True
        return None

    def set_unavailable(self, gender):
        if(gender in self.genders_available):
            self.genders_available[gender] = False
        return None

    def run(self, gender, error=False):
        if(self.game.debug):
            print("Emulating {}, {}, Round {}, {}.\n".format(self.parent.parent.get_name(), self.parent.get_name(), self.get_id(), gender))

        # Clear Screen
        self.game.clear_screen()

        # Show Error
        if(error):
            print("You have entered an invalid option.\n\n")

        # Menu Options
        print("Please select an option:")
        print("1. Input using file data")
        print("2. Input data manually")
        print("x. Save and Return")

        # Menu Response
        resp = input(">>> ")
        if(resp.isdigit()):
            if(resp == "1"):
                self.input_file(gender)
            elif(resp == "2"):
                self.input_manual(gender)
            else:
                return self.run(gender)
        elif(resp == "x"):
            self.game.save()
        else:
            return self.run(gender)
        Builder().reload_menu()

    def input_file(self, gender):
        # Validate Matches
        for match in self.get_matches(gender):
            match.validate_match(self.game.settings["score_limit"][gender], self.get_id(), True)

        # Print Matches
        for match in self.get_matches(gender):
            print(match.get_match_text())

            # Check for errors
            #if(match.validity()[0]):
            #    print("Error in this match: [{}] {}".format(match.get_match_text(), match.validity()[1]))
            #    match.validate_match(self.game.settings["score_limit"][gender], self.get_id(), True)

        # Mark next round as available
        next_round_id = self.get_id() + 1
        if(next_round_id <= self.game.settings['round_count']):
            self.parent.get_round(next_round_id).set_available(gender)

            if(self.game.debug):
                print("Set Season {}, Tour {}, Round {} for {} as available.".format(self.parent.parent.get_name(), self.parent.get_name(), next_round_id, gender))
        
        # Go back on the Main Menu
        Builder().go_back(True)

    def input_manual(self, gender):
        print("something else")