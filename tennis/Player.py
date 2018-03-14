"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""

class Player():
    name = None
    gender = None
    season = None

    def __init__(self, _name, _gender, _season):
        self.name = _name
        self.gender = _gender
        self.season = _season

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_season(self):
        return self.season

