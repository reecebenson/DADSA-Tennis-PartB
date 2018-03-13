"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""

class Match():
    # Variables
    game = None
    json_data = None
    gender = None
    player_one = None
    player_two = None
    player_one_score = None
    player_two_score = None
    winner = None

    def __init__(self, _game, _gender, _json_data):
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

    def get_match_text(self):
        return "[{0}] {1} - {2} [{3}] -- Winner: {4}".format(self.get_player_one()[0], self.get_player_one()[1], self.get_player_two()[0], self.get_player_two()[1], self.get_winner())
