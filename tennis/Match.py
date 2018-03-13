"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""

class Match():
    # Variables
    game = None
    parent = None
    json_data = None
    gender = None
    player_one = None
    player_two = None
    player_one_score = None
    player_two_score = None
    winner = None

    def __init__(self, _game, _gender, _parent, _json_data):
        self.parent = _parent
        self.gender = _gender
        self.game = _game
        self.json_data = _json_data

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
            else: # Error
                print("Something went wrong with the match data: {0}".format(_json_data))

        if(_game.debug):
            print("[ROUND]: Match '{0}-{1}' [{2}] made!".format(self.player_one, self.player_two, self.gender))

    def get_player_one(self):
        return [ self.player_one, self.player_one_score ]

    def get_player_two(self):
        return [ self.player_two, self.player_two_score ]

    def get_winner(self):
        return self.winner

    def get_match_text(self, full=False):
        return "{5}[{0}] {1} - {2} [{3}] -- Winner: {4}".format(self.get_player_one()[0], self.get_player_one()[1], self.get_player_two()[0], self.get_player_two()[1], self.get_winner(), "" if not full else "{0}, Round {1} -- ".format(self.parent.parent.get_name(), self.parent.get_id()))
    
    def get_match_as_json(self):
        return { self.player_one: self.player_one_score, self.player_two: self.player_two_score, "winner": self.winner }

    def validate_match(self, score_limit, round_id):
        # Clear Screen
        self.game.clear_screen()
        print(self.get_match_text(True))

        # Check Scores are not above limit
        if((self.player_one_score > score_limit) or (self.player_two_score > score_limit)):
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
            # Check if we're on the last round
            if(round_id is self.game.settings['round_count']):
                print("Player One [{0}] and Player Two [{1}] have the same score of {2}, please enter their new scores.".format(self.player_one, self.player_two, self.player_one_score))
                player_one_new_score = input("{0}: >>> ".format(self.player_one))
                player_two_new_score = input("{0}: >>> ".format(self.player_two))
                if(player_one_new_score.isdigit() and player_two_new_score.isdigit()):
                    self.player_one_score = int(player_one_new_score)
                    self.player_two_score = int(player_two_new_score)
                else:
                    return self.validate_match(score_limit, round_id)

            # Check in the next round for the winner
            else:
                print("Player One [{0}] and Player Two [{1}] have the same score of {2}, finding the winner through Round {3}...".format(self.player_one, self.player_two, self.player_one_score, round_id + 1))
                this_round_winners = self.parent.get_winners(self.gender)
                next_round_players = self.parent.parent.get_round(round_id + 1).get_players(self.gender)

                if(this_round_winners and next_round_players):
                    # Available Players
                    available_player = None
                    for p in next_round_players:
                        if(p not in this_round_winners):
                            available_player = p
                            break

                    print("Available Player: {0}\n\nThe winner of this match will be set to {0}.".format(available_player))

                    if(available_player is self.player_one):
                        self.winner = self.player_one
                        self.player_one_score = score_limit
                        self.player_two_score = score_limit - 1
                    elif(available_player is self.player_two):
                        self.winner = self.player_two
                        self.player_one_score = score_limit - 1
                        self.player_two_score = score_limit
                    else:
                        print("Modifying this player will corrupt the data.")
                    input(">>> Press <Return> to continue...")

        # Check there is atleast one winner
        winner_defined = True
        if((self.winner != self.player_one and self.winner != self.player_two) or (self.player_one_score != score_limit and self.player_two_score != score_limit)):
            winner_defined = False

        # Ensure there is a winner for this match
        if(not winner_defined):
            if(round_id is self.game.settings['round_count']):
                print("deh fuq is going on here, {0}.".format(self.get_match_text()))
            else:
                print("The scores for this match seem to be incomplete, finding the winner through Round {0}...".format(round_id + 1))
                this_round_winners = self.parent.get_winners(self.gender)
                next_round_players = self.parent.parent.get_round(round_id + 1).get_players(self.gender)

                if(this_round_winners and next_round_players):
                    # Available Players
                    available_player = None
                    for p in next_round_players:
                        if(p not in this_round_winners):
                            available_player = p
                            break

                    print("Available Player: {0}\n\nThe winner of this match will be set to {0}.".format(available_player))

                    if(available_player is self.player_one):
                        self.winner = self.player_one
                        self.player_one_score = score_limit
                        self.player_two_score = score_limit - 1
                    elif(available_player is self.player_two):
                        self.winner = self.player_two
                        self.player_one_score = score_limit - 1
                        self.player_two_score = score_limit
                    else:
                        print("Modifying this player will corrupt the data.")
                    input(">>> Press <Return> to continue...")

        return True