"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Round
from tennis.Colours import Colours

class Tournament():
    # Variables
    name = None
    game = None
    parent = None
    json_data = None
    rounds = None
    gender = None
    difficulty = None
    prize_money = None
    complete = None

    def __init__(self, _game, _name, _parent, _json_data):
        self.name = _name
        self.game = _game
        self.parent = _parent
        self.json_data = _json_data
        self.rounds = { }
        self.difficulty = _json_data['_difficulty']
        self.prize_money = _json_data['prize_money']
        self.complete = False

        # Read in Round Data
        for round_number in _json_data["rounds"]:
            round_data = _json_data["rounds"][round_number]
            
            # Load our Round in (if it is new)
            if(round_number not in self.rounds):
                # Create our Tournament Object
                self.rounds.update({ round_number: Round.Round(self.game, round_number, self, round_data) })

        if(_game.debug):
            print("[TOURNAMENT]: Tournament '{}' made!".format(_name))

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_rounds(self):
        return [ self.rounds[r] for r in self.rounds ]

    def get_round(self, round_id):
        return self.rounds["round_{0}".format(round_id)]

    def get_difficulty(self):
        return self.difficulty

    def get_prize_money(self):
        return self.prize_money

    def is_complete(self):
        return self.complete

    def set_complete(self, state):
        # Set this tournament as complete
        self.complete = state

        # Check if other tournaments are complete
        all_complete = True
        for t in self.parent.get_tournaments():
            if(not t.is_complete()):
                all_complete = False

        if(all_complete):
            # Open up the next season
            print("\n\nAll tournaments are now " + Colours.OKGREEN + "complete" + Colours.ENDC + "! Start opening season {}".format(self.parent.get_id() + 1))
            input(">>> Press <Return> to continue...")

            # Create New Season
            self.game.add_season(self.parent.get_id() + 1)