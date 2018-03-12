# DADSA - Assignment 1
# Reece Benson

from os import system as call

class Match():
    _round = None
    _id = None
    _winner = None
    _player_one = None
    _player_two = None
    _player_one_score = None
    _player_two_score = None
    
    def __init__(self, rnd, p_one, p_two, p_one_score, p_two_score):
        self._round = rnd
        self._id = len(rnd.matches())
        self._player_one = p_one
        self._player_two = p_two
        self._player_one_score = p_one_score
        self._player_two_score = p_two_score
    
    def id(self):
        return self._id

    def validate(self, error_count = 0):
        # Get our cap
        error = False
        cap = self.round().cap()
        
        # Check if the rounds are above the cap
        ## PLAYER ONE
        if(self.player_one()[1] > cap):
            # Error Occurred
            error = True
            error_count += 1

            # Print out the match for the user to see and reference to
            call("cls")
            print("Checking:", self.versuses(True))

            print("{0}'s score is above the cap of {1}, please enter this players new score:".format(self.player_one()[0].name(), cap))
            new_score = input(">>> ")
            if(new_score.isdigit()):
                new_score = int(new_score)
                if(new_score >= 0 and new_score <= cap):
                    self._player_one_score = new_score
                else:
                    return self.validate(error_count)
            else:
                return self.validate(error_count)
        
        ## PLAYER TWO
        if(self.player_two()[1] > cap):
            # Error Occurred
            error = True
            error_count += 1
            
            # Print out the match for the user to see and reference to
            call("cls")
            print("Checking:", self.versuses(True))
            
            print("{0}'s score is above the cap of {1}, please enter this players new score:".format(self.player_two()[0].name(), cap))
            new_score = input(">>> ")
            if(new_score.isdigit()):
                new_score = int(new_score)
                if(new_score >= 0 and new_score <= cap):
                    self._player_two_score = new_score
                else:
                    return self.validate(error_count)
            else:
                return self.validate(error_count)

        # Check if the scores of the players are the same
        if(self.player_one()[1] == self.player_two()[1]):
            # Error Occurred
            error = True
            error_count += 1
            
            # Print out the match for the user to see and reference to
            call("cls")
            print("Checking:", self.versuses(True))
            
            print("{0}'s and {1}'s score are the same. Please enter {1}'s new score:".format(self.player_one()[0].name(), self.player_two()[0].name()))
            new_score = input(">>> ")
            if(new_score.isdigit()):
                new_score = int(new_score)
                if(new_score >= 0 and new_score <= cap and new_score != self.player_two()[1]):
                    self._player_two_score = new_score
                else:
                    return self.validate(error_count)
            else:
                return self.validate(error_count)

        # Check that there is atleast one winner
        winnerExists = False
        if(self.player_one()[1] == cap or self.player_two()[1] == cap):
            winnerExists = True
        
        # There is not a winner available
        if(not winnerExists):
            # Error Occurred
            error = True
            error_count += 1
            
            # Print out the match for the user to see and reference to
            call("cls")
            print("Checking:", self.versuses(True))
            
            print("{0} vs. {1} does not have a winner. Please enter the new winner (by name):".format(self.player_one()[0].name(), self.player_two()[0].name()))
            new_winner = input(">>> ")
            if(new_winner.lower() == self.player_one()[0].name().lower()):
                self._player_one_score = cap
            elif(new_winner.lower() == self.player_two()[0].name().lower()):
                self._player_two_score = cap
            else:
                return self.validate(error_count)

        # Check if we're done (aggressive recursion)
        if(error):
            return self.validate(error_count)
        else:
            return error_count

    def round(self):
        return self._round

    def player_one(self):
        return [ self._player_one, self._player_one_score ]

    def player_two(self):
        return [ self._player_two, self._player_two_score ]

    def versuses(self, showScore = False):
        if(showScore):
            return "[{0}] {2} - {3} [{1}]".format(self.player_one()[0].name(), self.player_two()[0].name(), self.player_one()[1], self.player_two()[1])
        else:
            return "{0} vs. {1}".format(self.player_one()[0].name(), self.player_two()[0].name())
        return None

    def winner(self):
        if(self._player_one_score > self._player_two_score):
            self._winner = self.player_one()
            return self.player_one()
        else:
            self._winner = self.player_two()
            return self.player_two()
        return None