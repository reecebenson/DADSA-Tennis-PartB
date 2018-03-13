"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
# Imports
import json
from tennis.SmallJSON import SmallJSON

class File():
    @staticmethod
    def update_season(season, new_data):
        with open('./data/json/game.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data["seasons"]):
                # Update our season data
                data["seasons"][season] = new_data

                # Seek back to SOF and write back our data
                f.seek(0)
                f.write(json.dumps(data, indent=4, cls=SmallJSON))
                f.truncate()
                return True
            else:
                return False
        return True

