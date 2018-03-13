"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
# Imports
import json
from tennis import Season

# Variables
gamePath = "./data/json/game.json"
settingsPath = "./data/json/settings.json"

class Game():
    game = None
    seasons = None

    def __init__(self, game):
        self.game = game
        self.seasons = { }

    def load(self):
        with open(gamePath) as game_file:
            game_data = json.load(game_file)
            seasons = game_data["seasons"]

            for season in seasons:
                # Load our Season in (if it is new)
                if(season not in self.seasons):
                    # Create our Season Object
                    self.seasons.update({ season: Season.Season(self.game, season, seasons[season]) })