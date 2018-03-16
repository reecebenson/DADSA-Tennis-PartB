"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Match
from tennis.Menu import Menu
from tennis.Menu import Builder
from functools import partial

class MatchGender():
    # Variables
    game = None
    gender = None
    parent = None
    matches = None
    available = None
    input_file_state = None

    def __init__(self, _game, _gender, _parent):
        # Set Variables
        self.game = _game
        self.gender = _gender
        self.parent = _parent
        self.matches = [ ]
        
        # Set Flags
        self.available = False
        self.input_file_state = True

    def add_match(self, match):
        self.matches.append(Match.Match(self.game, self.gender, self, match))

    def get_gender(self):
        return self.gender

    def is_available(self):
        return self.available

    def set_availability(self, availability):
        self.available = availability

    def is_input_file_allowed(self):
        return self.input_file_state

    def set_input_file_state(self, state):
        self.input_file_state = state

    def get_matches(self):
        return [ m for m in self.matches ]

    def get_players(self):
        players = [ ]
        for m in self.get_matches():
            players.append(m.player_one)
            players.append(m.player_two)
        return players

    def get_winners(self,):
        return [ m.get_winner() for m in self.get_matches() ]

    def run(self, error=False):
        if(self.game.debug):
            print("Emulating {}, {}, Round {}, {}.\n".format(self.parent.parent.parent.get_name(), self.parent.parent.get_name(), self.parent.get_id(), self.gender))

        # Clear Screen
        self.game.clear_screen()

        # Show Error
        if(error):
            print("You have entered an invalid option.\n\n")

        # Menu Options
        print("Please select an option:")
        print("1. Input using file data{}".format("" if self.is_input_file_allowed() else " (Not Available)"))
        print("2. Input data manually")
        print("x. Save and Return")

        # Menu Response
        resp = input(">>> ")
        if(resp.isdigit()):
            if(resp == "1"):
                if(self.is_input_file_allowed()):
                    self.input_file()
                else:
                    self.run(True)
            elif(resp == "2"):
                self.input_manual()
            else:
                return self.run(True)
        elif(resp == "x"):
            self.game.save()
        else:
            return self.run(True)
        Builder().reload_menu()

    def input_file(self):
        # Validate Matches
        for match in self.get_matches():
            match.validate_match(self.game.settings["score_limit"][self.gender], self.parent.get_id(), True)

        # Clear Screen
        self.game.clear_screen()

        # Print Matches
        for match in self.get_matches():
            print(match.get_match_text())

        # Mark next round as available
        next_round_id = self.parent.get_id() + 1
        if(next_round_id <= self.game.settings['round_count']):
            self.parent.parent.get_round(next_round_id).get_gender(self.gender)[1].set_availability(True)

            if(self.game.debug):
                print("\nSet Season {}, Tour {}, Round {} for {} as available.".format(self.parent.parent.parent.get_name(), self.parent.parent.get_name(), next_round_id, self.gender))
        
        # Go back on the Main Menu
        Builder().go_back(True)

    def input_manual(self, gender):
        print("something else")
