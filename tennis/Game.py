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
playersPath = "./data/json/players.json"
rankingPointsPath = "./data/json/rankingPoints.json"

class Game():
    game = None
    parent = None
    debug = False
    seasons = None
    settings = None

    def __init__(self, _parent):
        self.game = self
        self.parent = _parent
        self.seasons = { }
        self.settings = { }

    def load(self):
        with open(settingsPath) as settings_file:
            self.settings = json.load(settings_file)

        with open(gamePath) as game_file:
            game_data = json.load(game_file)
            seasons = game_data["seasons"]

            for season in seasons:
                # Load our Season in (if it is new)
                if(season not in self.seasons):
                    # Get our Players
                    season_players = None
                    with open(playersPath) as players_file:
                        season_players = json.load(players_file)

                    # Create our Season Object
                    new_season = Season.Season(self.game, season, seasons[season], season_players)

                    # Update our Seasons List
                    self.seasons.update({ season: new_season })

    def exit(self):
        self.parent.exit()

    def clear_screen(self):
        call("cls")
