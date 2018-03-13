"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""

class Player():
    name = None
    gender = None

    def __init__(self, _name, _gender):
        self.name = _name
        self.gender = _gender

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

