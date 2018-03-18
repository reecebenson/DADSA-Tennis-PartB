"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis.Colours import Colours

class Match():
    # Variables
    game = None
    name = None
    parent = None
    json_data = None
    gender = None
    player_one = None
    player_two = None
    player_one_score = None
    player_two_score = None
    player_one_object = None
    player_two_object = None
    winner = None
    invalid = None
    invalid_reason = None

    def __init__(self, _game, _gender, _parent, _json_data):
        self.name = Colours.BOLD + "Season {0}, Tournament {1}, Round {2}, Match {3} of {4}s.".format(_parent.parent.parent.parent.get_id(), _parent.parent.parent.get_name(), _parent.parent.get_id(), len(_parent.matches) + 1, _gender) + Colours.ENDC
        self.parent = _parent
        self.gender = _gender
        self.game = _game
        self.limit = _game.settings["score_limit"][_gender]
        self.json_data = _json_data

        self.invalid = False
        self.invalid_reason = None

        # Parse Match Data
        for i,name in enumerate(_json_data):
            if(i == 0): # Player One
                self.player_one = name
                self.player_one_score = _json_data[name]
            elif(i == 1): # Player Two
                self.player_two = name
                self.player_two_score = _json_data[name]
            elif(i == 2): # Winner
                self.winner = _json_data[name]
                self.validate_winner()
            else: # Error
                print("Something went wrong with the match data: {0}".format(_json_data))

        # Apply Player Objects
        self.player_one_object = self.parent.parent.parent.parent.get_player(self.player_one, _gender)
        self.player_two_object = self.parent.parent.parent.parent.get_player(self.player_two, _gender)

        if(_game.debug):
            print("[ROUND]: Match '{0}-{1}' [{2}] made! [{3}:{5} -- {4}:{6}]".format(self.player_one, self.player_two, self.gender, self.player_one_object, self.player_two_object, self.player_one_object.get_name(), self.player_two_object.get_name()))

    def get_name(self):
        return self.name

    def get_text(self):
        return "{}\n{}\n".format(self.get_name(), self.get_match_text())

    def get_player_one(self):
        return [ self.player_one, self.player_one_score ]

    def get_player_two(self):
        return [ self.player_two, self.player_two_score ]

    def get_winner(self):
        return self.winner

    def get_match_text(self, full=False):
        return "{5}[{6}{0}{7}] {1} - {2} [{6}{3}{7}] -- Winner: {8}{4}{7}".format(self.get_player_one()[0], self.get_player_one()[1], self.get_player_two()[1], self.get_player_two()[0], self.get_winner(), "" if not full else "{0}, Round {1} -- ".format(self.parent.parent.parent.get_name(), self.parent.parent.get_id()), Colours.OKBLUE, Colours.ENDC, Colours.OKGREEN)
    
    def get_match_bonuses(self):
        # Variables
        bonuses = self.game.settings["score_bonus"][self.gender]

        # Define Scores as Format (x,y)
        scores = "{0},{1}".format(self.player_one_score, self.player_two_score)

        # Get Score Response
        if(scores in bonuses):
            return (bonuses[scores][0], bonuses[scores][1])
        return None

    def get_match_bonuses_text(self):
        # Variables
        bonuses = self.game.settings["score_bonus"][self.gender]

        # Define Scores as Format (x,y)
        scores = "{0},{1}".format(self.player_one_score, self.player_two_score)

        # Get Score Response
        if(scores in bonuses):
            print("\tBonus Found! {0} for {1}".format(bonuses[scores][0], bonuses[scores][1]))

    def get_match_as_json(self):
        return { self.player_one: self.player_one_score, self.player_two: self.player_two_score, "winner": self.winner }

    def validity(self):
        return (self.invalid, self.invalid_reason)

    def validate_winner(self):
        winner_found = False
        if(self.player_one_score == self.limit):
            winner_found = True
            self.winner = self.player_one

        if(self.player_two_score == self.limit):
            winner_found = True
            self.winner = self.player_two

        if(not winner_found):
            self.winner = "injury"

        if(self.player_one_score == self.limit and self.player_two_score == self.limit):
            self.winner = "dupe"

        if(self.player_one_score > self.limit or self.player_two_score > self.limit):
            self.winner = "badscore"

    def validate_match(self, score_limit, round_id, user_validate=False):
        # Reset Invalidity
        error = False
        self.invalid = False
        self.invalid_reason = None

        # Clear Screen
        if(not self.game.debug):
            print("Validating Match:", self.get_match_text(True))
            
        # Validate Winner Tag
        self.validate_winner()

        # Check Scores are not above limit
        if((self.player_one_score > score_limit) or (self.player_two_score > score_limit)):
            self.invalid = True
            self.invalid_reason = "above_score_limit"
            
            if(user_validate):
                error = True
                self.game.clear_screen()
                if(self.player_one_score > score_limit):
                    print("Player One [{0}] has a score of {1} whereas the limit is {2}, please enter a new score.".format(self.player_one, self.player_one_score, score_limit))
                    player_one_new_score = input(">>> ")
                    if(player_one_new_score.isdigit()):
                        self.player_one_score = int(player_one_new_score)
                    else:
                        return self.validate_match(score_limit, round_id)

                if(self.player_two_score > score_limit):
                    print("Player Two [{0}] has a score of {1} whereas the limit is {2}, please enter a new score.".format(self.player_two, self.player_two_socre, score_limit))
                    player_two_new_score = input(">>> ")
                    if(player_two_new_score.isdigit()):
                        self.player_two_score = int(player_two_new_score)
                    else:
                        return self.validate_match(score_limit, round_id)

        # Check Scores are not the same
        if(self.player_one_score is self.player_two_score):
            self.invalid = True
            self.invalid_reason = "same_scores"
            
            if(user_validate):
                error = True
                self.game.clear_screen()
                print(self.get_text())

                # Check if we're on the last round
                if(round_id is self.game.settings['round_count']):
                    print("Player One [{3}{0}{4}] and Player Two [{3}{1}{4}] have the same score of {2}, please enter their new scores.".format(self.player_one, self.player_two, self.player_one_score, Colours.OKBLUE, Colours.ENDC))
                    self.player_scores_manual_input()

                # Check in the next round for the winner
                else:
                    # Get next rounds winner
                    this_round_winners = self.parent.get_winners()
                    next_round_players = self.parent.parent.parent.get_round(round_id + 1).get_gender(self.gender)[1].get_players()
                    available_player = None

                    if(this_round_winners and next_round_players):
                        # Available Players
                        for p in next_round_players:
                            if(p not in this_round_winners):
                                available_player = p
                                break

                    print("Player One [{3}{0}{4}] and Player Two [{3}{1}{4}] have the same score of {2}.".format(self.player_one, self.player_two, self.player_one_score, Colours.OKBLUE, Colours.ENDC))
                    self.find_available_player(score_limit, round_id)

        # Check there is atleast one winner
        winner_defined = True
        if((self.winner != self.player_one and self.winner != self.player_two) or (self.player_one_score != score_limit and self.player_two_score != score_limit)):
            winner_defined = False
            self.invalid = True
            self.invalid_reason = "no_winner"

        # Ensure there is a winner for this match
        if(not winner_defined and user_validate):
            error = True
            self.game.clear_screen()
            if(round_id is self.game.settings['round_count']):
                print(self.get_text())
                print("Unable to set a winner for this match as it is on the last round: {0}".format(self.get_match_text()))
                exit()
            else:
                print(self.get_text())
                print("The scores for this match seem to be incomplete, finding the winner through Round {0} (score lmiit: {1})...".format(round_id + 1, score_limit))
                self.find_available_player(score_limit, round_id)

        # Intensive Recursion
        if(error):
            return self.validate_match(score_limit, round_id, user_validate)
        else:
            return True

    def find_available_player(self, score_limit, round_id):
        # Get next rounds winner
        this_round_winners = self.parent.get_winners()
        next_round_players = self.parent.parent.parent.get_round(round_id + 1).get_gender(self.gender)[1].get_players()
        available_player = None

        if(this_round_winners and next_round_players):
            # Available Players
            for p in next_round_players:
                if(p not in this_round_winners):
                    available_player = p
                    break

            if(available_player is not None):
                print("Available Player: {1}{0}{2}\n\nThe winner of this match will be set to {1}{0}{2}, confirm? [Y/n]".format(available_player, Colours.OKBLUE, Colours.ENDC))
                resp = input(">>> ")
                if(resp == "y" or resp == ""):
                    self.player_scores_find(available_player, score_limit, round_id)
                else:
                    self.player_scores_manual_input(score_limit, round_id)

    def player_scores_find(self, available_player, score_limit, round_id):
        if(available_player == self.player_one):
            self.winner = self.player_one
            self.player_one_score = score_limit
            self.player_two_score = score_limit - 1
            return True
        elif(available_player == self.player_two):
            self.winner = self.player_two
            self.player_one_score = score_limit - 1
            self.player_two_score = score_limit
            return True
        else:
            print("Modifying this player will corrupt the data, skipping...")
        return False

    def player_scores_manual_input(self, score_limit, round_id):
        print("Please enter the players new scores:")
        player_one_new_score = input("{0}: >>> ".format(self.player_one))
        player_two_new_score = input("{0}: >>> ".format(self.player_two))
        if(player_one_new_score.isdigit() and player_two_new_score.isdigit()):
            # Set Scores
            self.player_one_score = int(player_one_new_score)
            self.player_two_score = int(player_two_new_score)

            # Set Winner
            if(self.player_one_score > self.player_two_score):
                self.winner = self.player_one
            elif(self.player_two_score > self.player_one_score):
                self.winner = self.player_two
            else:
                return self.validate_match(score_limit, round_id)

            # Validate Next Rounds
            next_round_id = round_id + 1
            if(next_round_id <= self.game.settings['round_count']):
                next_round_players = self.parent.parent.parent.get_round(next_round_id).get_gender(self.gender)[1].get_players()

                # Check that the winner is within the next round
                if(self.winner not in next_round_players):
                    print("\nYou have selected {0}, who is not a valid participant within the next round.\nDue to this, all future rounds within this tournament will require manual input.".format(self.winner))
                    # Set Manual Input for next rounds
                    for t_round in self.parent.parent.parent.get_rounds():
                        if(t_round.get_id() > round_id):
                            match_gender = t_round.get_gender(self.gender)[1]
                            match_gender.set_input_file_state(False)
                else:
                    print("\nThe winner you have chosen has kept the future rounds data complete, you will have the ability to continue reading from the file for future rounds.")
                input(">>> Press <Return> to continue...")
            else:
                print("too high of a round", self.parent.parent.get_id(), next_round_id)
        else:
            return self.validate_match(score_limit, round_id)