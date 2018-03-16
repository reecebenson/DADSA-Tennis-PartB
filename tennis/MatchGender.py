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
    complete = None
    input_file_state = None
    pop_player_list = None

    def __init__(self, _game, _gender, _parent):
        # Set Variables
        self.game = _game
        self.gender = _gender
        self.parent = _parent
        self.matches = [ ]
        
        # Set Flags
        self.pop_player_list = None
        self.available = False
        self.complete = False
        self.input_file_state = True

    def add_match(self, match):
        m = Match.Match(self.game, self.gender, self, match)
        self.matches.append(m)
        return m

    def get_gender(self):
        return self.gender

    def is_complete(self):
        return self.complete

    def set_complete(self, state):
        self.complete = state

    def is_available(self):
        return self.available

    def set_availability(self, state):
        self.available = state

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

    def get_winners(self):
        return [ m.get_winner() for m in self.get_matches() ]

    def set_next_round_as_available(self):
        # Mark next round as available
        next_round_id = self.parent.get_id() + 1
        if(next_round_id <= self.game.settings['round_count']):
            self.parent.parent.get_round(next_round_id).get_gender(self.gender)[1].set_availability(True)

            if(self.game.debug):
                print("\nSet Season {}, Tour {}, Round {} for {} as available.".format(self.parent.parent.parent.get_name(), self.parent.parent.get_name(), next_round_id, self.gender))
        
            return True
        return False

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
        print("1. View Round{}".format("" if self.is_complete() else " (Not Available)"))
        print("2. Input using file data{}".format("" if (self.is_input_file_allowed() and not self.is_complete()) else " (Not Available)"))
        print("3. Input data manually{}".format("" if not self.is_complete() else " (Not Available)"))
        print("x. Save and Return")

        # Menu Response
        resp = input(">>> ")
        if(resp.isdigit()):
            if(resp == "1"):
                if(self.is_complete()):
                    self.view()
                else:
                    self.run(True)
            elif(resp == "2"):
                if(self.is_input_file_allowed() and not self.is_complete()):
                    self.input_file()
                else:
                    self.run(True)
            elif(resp == "3"):
                if(not self.is_complete()):
                    self.input_manual()
                else:
                    self.run(True)
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

    def view(self):
        print("Running matches...")

        # Validate Matches
        for match in self.get_matches():
            match.validate_match(self.game.settings["score_limit"][self.gender], self.parent.get_id(), True)

        # Print Matches
        for match in self.get_matches():
            print(match.get_match_text())

        input("hold")

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
        self.set_complete(True)
        self.set_next_round_as_available()

        # Go back on the Main Menu
        Builder().go_back(True)
        input(">>> Press <Return> to continue...")

    def input_manual(self):
        # Players
        if(self.pop_player_list is None):
            self.pop_player_list = self.get_players()
            self.inputted_matches = [ ]

        # Disable File Input
        self.set_input_file_state(False)

        # Print Instructions
        error = False
        while(len(self.pop_player_list) is not 0):
            # Clear Screen
            self.game.clear_screen()

            # Cache Player List
            cached_player_list = self.pop_player_list[:]

            # Print Previous Matches
            if(len(self.inputted_matches) > 0):
                print("Current matches created:")
                for m in self.inputted_matches:
                    print("[{0}] {1} - {2} [{3}]".format(m['player_one'], m['player_one_score'], m['player_two_score'], m['player_two']))
                print()

            # Print Player List
            c = 0
            print("Available Players to create for Round {}".format(self.parent.get_id()))
            for p in self.pop_player_list:
                print("[{0}{1}{2}] {3}{4}{2}".format(Colours.OKGREEN, f"{c:02}", Colours.ENDC, Colours.BOLD, p), end='{}'.format("\n" if (((c+1) % 4) == 0 or c+1 == len(self.pop_player_list)) else " "))
                c += 1

            # Has Errored
            if(error):
                print("\n{0}{1}Error:{2}\n{0}You have entered an invalid value, please refer to the format.{2}".format(Colours.FAIL, Colours.BOLD, Colours.ENDC))
                error = False

            # Ask for Player Names
            print("\nPlease enter 2 player names in the following format: \"MP01,MP15\":")
            resp = input(">>> ")
            player_names = resp.upper().replace(" ", "").split(",")

            # Pop Players Names from the list
            if(len(player_names) == 2):
                if(player_names[0] in self.pop_player_list):
                    self.pop_player_list.remove(player_names[0])
                else:
                    self.pop_player_list = cached_player_list
                    error = True
                    continue

                if(player_names[1] in self.pop_player_list):
                    self.pop_player_list.remove(player_names[1])
                else:
                    self.pop_player_list = cached_player_list
                    error = True
                    continue
            else:
                error = True
                continue

            # Ask for Player Scores
            print("\nPlease enter the scores for {} vs. {}: \"{}-0\":".format(player_names[0], player_names[1], self.game.settings["score_limit"][self.gender]))
            resp = input(">>> ")
            player_scores = resp.replace(" ", "").split("-")

            # Validate Scores as Integers/Digits
            player_one_score = None
            player_two_score = None
            if(len(player_scores) == 2):
                if(player_scores[0].isdigit()):
                    player_one_score = int(player_scores[0])

                if(player_scores[1].isdigit()):
                    player_two_score = int(player_scores[1])

                if(player_one_score is None or player_two_score is None):
                    self.pop_player_list = cached_player_list
                    error = True
                    continue
            else:
                self.pop_player_list = cached_player_list
                error = True
                continue

            # Add match to temporary match list
            self.inputted_matches.append({ 'player_one': player_names[0], 'player_two': player_names[1], 'player_one_score': player_one_score, 'player_two_score': player_two_score })
            input("\nMatch Created: [{}] {} - {} [{}], press <Return> to continue...".format(player_names[0], player_scores[0], player_scores[1], player_names[1]))

        if((len(self.pop_player_list) == 0) and (len(self.inputted_matches) == len(self.get_players()) / 2)):
            # Set Flags
            self.set_complete(True)
            self.set_next_round_as_available()

            # Set Manual Input for next rounds
            for t_round in self.parent.parent.get_rounds():
                if(t_round.get_id() > self.parent.get_id()):
                    match_gender = t_round.get_gender(self.gender)[1]
                    match_gender.set_input_file_state(False)

            # Clear our Matches
            self.matches = [ ]
            for m in self.inputted_matches:
                m = self.add_match({ m['player_one']: m['player_one_score'], m['player_two']: m['player_two_score'], "winner": 'unknown' })
                m.validate_match(self.game.settings['score_limit'][self.gender], self.parent.get_id(), True)
        else:
            input("should never get here")

        input(Colours.OKGREEN + "\n>>> Press <Return> to continue..." + Colours.ENDC)
