import json
from classes.SmallJSON import SmallJSON

class File():
    @staticmethod
    def update_tournament_rounds(season, tournament, new_rounds):
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data):
                # Check our Tournament exists
                if(tournament in data[season]["tournaments"]):
                    # Append our new_rounds to the current data
                    data[season]["tournaments"][tournament]['rounds'] = new_rounds

                    # Seek back to SOF and write back our data
                    f.seek(0)
                    f.write(json.dumps(data, indent=4, cls=SmallJSON))
                    f.truncate()
                else:
                    return False
            else:
                return False
        return True
    
    @staticmethod
    def update_settings(season, name, value):
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data):
                # Check if our setting exists
                if(name in data[season]['settings']):
                    # Update setting
                    data[season]['settings'][name] = value
                else:
                    # Create setting
                    data[season]['settings'].update({ name: value })

                # Seek back to SOF and write back our data
                f.seek(0)
                f.write(json.dumps(data, indent=4, cls=SmallJSON))
                f.truncate()
            else:
                return False
        return True
    
    @staticmethod
    def get_global_setting(name):
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            if("settings" in data):
                if(name in data["settings"]):
                    return data["settings"][name]
            
            return None

    @staticmethod
    def get_seasons():
        seasonIds = [ ]
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            for season in data:
                if(season == "settings"):
                    continue
                seasonIds.append(season)
            
        return seasonIds

    @staticmethod
    def update_global_settings(name, value):
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            # Check if our setting exists
            if(name in data['settings']):
                # Update setting
                data['settings'][name] = value
            else:
                # Create setting
                data['settings'].update({ name: value })

            # Seek back to SOF and write back our data
            f.seek(0)
            f.write(json.dumps(data, indent=4, cls=SmallJSON))
            f.truncate()
        return True

    @staticmethod
    def update_file_saving(season, tournament, value):
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data):
                # Check our tournament exists
                if(tournament in data[season]["tournaments"]):
                    # Set our Setting
                    data[season]["tournaments"][tournament]["_file_saving"] = value

                    # Seek back to SOF and write back our data
                    f.seek(0)
                    f.write(json.dumps(data, indent=4, cls=SmallJSON))
                    f.truncate()
                else:
                    return False
            else:
                return False
