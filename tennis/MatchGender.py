"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Match
from tennis.Menu import Menu
from tennis.Menu import Builder
from tennis.Colours import Colours
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
            print("\nError:\nYou have entered an invalid option.\n\n")

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
        elif(resp == "x" or resp == "b"):
            self.game.save()
            Builder().reload_menu()
            return "SKIP"
        else:
            return self.run(True)

        # Recursive Menu
        return self.run()

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
        input(">>> Press <Return> to continue...")

    def input_manual(self):

        # Players
        pop_player_list = self.get_players()

        # Print Instructions
        while(len(pop_player_list) is not 0):
            # Clear Screen
            self.game.clear_screen()

            # Print Player List
            c = 0
            for p in pop_player_list:
                print("[{0}{1}{2}] {3}{4}{2}".format(Colours.OKGREEN, f"{c:02}", Colours.ENDC, Colours.BOLD, p), end='{}'.format("\n" if (((c+1) % 4) == 0) else " "))
                c += 1

            # Instructions
            print("\nPlease enter 2 players identifiers in the format: \"00,14\":")
            resp = input(">>> ")
            player_names = resp.replace(" ", "").split(",")

            # Pop Players Names from the list
            if(player_names[0] in pop_player_list):
                pop_player_list.remove(player_names[0])
            else:
                continue

            if(player_names[1] in pop_player_list):
                pop_player_list.remove(player_names[1])
            else:
                pop_player_list.append(player_names[0])
                continue

            print("\nPlease enter the scores for {} vs. {}: \"2,1\":".format())
            resp = input(">>> ")
            player_names = resp.replace(" ", "").split(",")

            

        input(Colours.OKGREEN + "\n>>> Press <Return> to continue..." + Colours.ENDC)
