"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""

class Player():
    name = None
    gender = None
    season = None
    win_count = None

    def __init__(self, _name, _gender, _season):
        self.name = _name
        self.gender = _gender
        self.season = _season
        self.win_count = 0

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_season(self):
        return self.season

    def get_wins(self):
        return self.win_count

    def increment_wins(self):
        self.win_count += 1
        return self.get_wins()
