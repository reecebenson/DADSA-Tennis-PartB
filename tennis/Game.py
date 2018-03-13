"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
# Imports
import json
from os import system as call
from tennis import Season

# Variables
gamePath = "./data/json/game.json"
settingsPath = "./data/json/settings.json"

class Game():
    debug = True
    seasons = None
    settings = None

    def __init__(self):
        self.game = self
        self.seasons = { }
        self.settings = { }

    def clear_screen(self):
        call("cls")

    def load(self):
        with open(settingsPath) as settings_file:
            self.settings = json.load(settings_file)

        with open(gamePath) as game_file:
            game_data = json.load(game_file)
            seasons = game_data["seasons"]

            for season in seasons:
                # Load our Season in (if it is new)
                if(season not in self.seasons):
                    # Create our Season Object
                    self.seasons.update({ season: Season.Season(self.game, season, seasons[season]) })