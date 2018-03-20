"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
import json
import cProfile
from tennis.File import File
from tennis.Player import Player
from tennis import Tournament
from tennis.Colours import Colours

class Season():
    # Variables
    name = None
    id = None
    game = None
    json_data = None
    tournaments = None
    players = None
    available = None

    def __init__(self, _game, _name, _json_data, _players):
        self.name = _name
        self.id = int(_name[-1:])
        self.game = _game
        self.json_data = _json_data
        self.tournaments = { }
        self.players = { }
        self.genders = [ ]
        self.available = True if self.id == 1 else False

        # Set our Players
        self.set_players(_players)

        # Read in Tournament Data
        for tournament in _json_data["tournaments"]:
            tournament_data = _json_data["tournaments"][tournament]

            # Load our Tournament in (if it is new)
            if(tournament not in self.tournaments):
                # Create our Tournament Object
                self.tournaments.update({ tournament: Tournament.Tournament(self.game, tournament, self, tournament_data) })

        if(_game.debug):
            print("[SEASON]: Season '{}' made!".format(_name))

        self.validate_season()

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_tournaments(self):
        return [ self.tournaments[t] for t in self.tournaments ]

    def get_tournament(self, tournament_name):
        return self.tournaments[tournament_name]

    def is_available(self):
        return self.available

    def set_availability(self, state):
        self.available = state

    def set_players(self, player_list):
        for gender in player_list[self.get_name()]:
            # Add Gender to Genders List
            if(gender not in self.genders):
                self.genders.append(gender)

            # Add Gender to Players List
            if(gender not in self.players):
                self.players.update({ gender: [ ] })

            # Create Player
            for player in player_list[self.get_name()][gender]:
                p = Player(player, gender, self)
                self.players[gender].append(p)

    def get_players(self, gender):
        return self.players[gender] if gender in self.players else [ ]
    
    def get_player(self, name, gender):
        if(gender in self.players):
            for player in self.players[gender]:
                if(player.get_name() == name):
                    return player
        return None

    def list_players(self):
        print("Season: {}\n".format(self.get_name()))
        for gender in self.players:
            print("Gender: {}, count: {}".format(gender, len(self.players[gender])))
            print("{0}\n".format(", ".join([ player.get_name() for player in self.players[gender] ])))

    def statistical_analysis(self, error=False, gender=None):
        # Clear Screen
        self.game.clear_screen()

        # Has Errored
        if(error and gender is None):
            print("\n{0}{1}Error:{2}\n{0}You have entered an invalid value, please refer to the format.{2}\n".format(Colours.FAIL, Colours.BOLD, Colours.ENDC))
            error = False

        # Select a Gender
        selected_gender = gender
        if(selected_gender is None):
            index = 0
            print(Colours.BOLD + "Please select a gender:" + Colours.ENDC)
            for gender in self.genders:
                index += 1
                print("{2}{0}{3}. {1}".format(index, gender.title(), Colours.OKGREEN, Colours.ENDC))
            print("{0}b{1}. Back".format(Colours.FAIL, Colours.ENDC))

            selected_gender = input(">>> ")
        
        if(type(selected_gender) is int or selected_gender.isdigit()):
            if(int(selected_gender) > 0 and int(selected_gender) <= len(self.genders)):
                # Update Variable
                selected_gender = int(selected_gender)

                # Clear Screen
                self.game.clear_screen()

                # Has Errored
                if(error):
                    print("\n{0}{1}Error:{2}\n{0}You have entered an invalid option.{2}\n".format(Colours.FAIL, Colours.BOLD, Colours.ENDC))
                    error = False

                # Select a Statistical Type
                print(Colours.BOLD + "Please select a statistic to view:" + Colours.ENDC)
                print("{0}1{1}. Number of wins for a player with a particular score".format(Colours.OKGREEN, Colours.ENDC))
                print("{0}2{1}. The percentage wins of a player".format(Colours.OKGREEN, Colours.ENDC))
                print("{0}3{1}. Show the player(s) with the most wins".format(Colours.OKGREEN, Colours.ENDC))
                print("{0}4{1}. Show the player(s) with the most losts".format(Colours.OKGREEN, Colours.ENDC))
                print("{0}b{1}. Back".format(Colours.FAIL, Colours.ENDC))
                
                selected_stat = input(">>> ")
                if(selected_stat.isdigit()):
                    if(int(selected_stat) > 0 and int(selected_stat) <= 4):
                        # Update Variable
                        selected_stat = int(selected_stat)

                        # Clear Screen
                        self.game.clear_screen()

                        # Select Tournament
                        print(Colours.BOLD + "Please select a tournament:" + Colours.ENDC)
                        i = 1
                        for t in self.get_tournaments():
                            print("{0}{1}{2}. {3}".format(Colours.OKGREEN, i, Colours.ENDC, t.get_name()))
                            i += 1
                        print("{0}{1}{2}. {3}All{2}".format(Colours.OKGREEN, i, Colours.ENDC, Colours.BOLD))

                        selected_tournament = input(">>> ")
                        if(selected_tournament.isdigit() and (int(selected_tournament) > 0 and int(selected_tournament) <= i)):
                            # All Tournaments
                            if(int(selected_tournament) == i):
                                selected_tournament = "ALL"
                            else:
                                selected_tournament = self.get_tournaments()[int(selected_tournament)-1]
                        else:
                            return self.statistical_analysis(True, selected_gender)

                        # Clear Screen
                        self.game.clear_screen()

                        # Title
                        print(Colours.BOLD + "Selected Tournament: " + Colours.ENDC + Colours.OKBLUE + (selected_tournament.get_name() if type(selected_tournament) is not str else "All") + Colours.ENDC + "\n")

                        # Select Player
                        if(selected_stat == 1 or selected_stat == 2):
                            c = 0
                            for p in self.get_players(self.genders[selected_gender-1]):
                                print("[{0}-{2}] {3}{4}{2}".format(Colours.OKGREEN, f"{c:02}", Colours.ENDC, Colours.BOLD, p.get_name()), end='{}'.format("\n" if (((c+1) % 4) == 0 or c+1 == len(self.get_players(self.genders[selected_gender-1]))) else " "))
                                c += 1

                            print(Colours.BOLD + "\nPlease select a player: (Example: \"MP01\")" + Colours.ENDC)
                            selected_player = input(">>> ")
                            temp_player_list = [ p.get_name() for p in self.get_players(self.genders[selected_gender-1]) ]
                            if(selected_player.upper() in temp_player_list):
                                plyr = self.get_player(selected_player.upper(), self.genders[selected_gender-1])

                                # Number of wins for a player with a particular score
                                if(selected_stat == 1):
                                    not_finished = True
                                    ss_error = False
                                    while(True and not_finished):
                                        # Error
                                        if(ss_error):
                                            print("\n{0}{1}Error:{2}\n{0}You have entered an invalid option.{2}\n".format(Colours.FAIL, Colours.BOLD, Colours.ENDC))
                                            ss_error = False

                                        print("\n{1}Please enter the score to search for: (Example: \"{0}-0\"){2}".format(self.game.settings['score_limit'][self.genders[selected_gender-1]], Colours.BOLD, Colours.ENDC))
                                        score_search = input(">>> ")

                                        # Analyse Input
                                        scores = score_search.split("-")

                                        # Error Checks
                                        if(len(scores) != 2):
                                            ss_error = True
                                            continue
                                        
                                        if(not scores[0].isdigit() or not scores[1].isdigit()):
                                            ss_error = True
                                            continue
                                        else:
                                            scores[0] = int(scores[0])
                                            scores[1] = int(scores[1])

                                        if(scores[0] > self.game.settings['score_limit'][self.genders[selected_gender-1]] or scores[1] > self.game.settings['score_limit'][self.genders[selected_gender-1]]):
                                            ss_error = True
                                            continue

                                        # Find Matches
                                        print("\nFinding matches for {2}{0}{3} with the scores {2}{1}{3}{4}...".format(plyr.get_name(), score_search, Colours.OKBLUE, Colours.ENDC, " in tournament {1}{0}{2}".format(selected_tournament.get_name() if (type(selected_tournament) is not str) else "", Colours.OKBLUE, Colours.ENDC) if selected_tournament != "ALL" else ""))

                                        # All Tournaments
                                        if(type(selected_tournament) is str):
                                            print()
                                            for t in self.get_tournaments():
                                                print("[{0}{1}{2}]:".format(Colours.OKBLUE, t.get_name(), Colours.ENDC))
                                                matches_found = False
                                                for r in t.get_rounds():
                                                    mg = r.get_gender(self.genders[selected_gender-1])[1]

                                                    if(not mg.is_complete()):
                                                        print(Colours.GRAY + "\t(Round {0} is incomplete, so data has not been pulled from here)".format(r.get_id()) + Colours.ENDC)
                                                    else:
                                                        for m in mg.get_matches():
                                                            plyr_one = m.get_player_one()
                                                            plyr_two = m.get_player_two()

                                                            if((plyr_one[0] == plyr.get_name() and plyr_one[1] == scores[0] and plyr_two[1] == scores[1]) or (plyr_two[0] == plyr.get_name() and plyr_one[1] == scores[1] and plyr_two[1] == scores[0])):
                                                                print(Colours.GRAY + "\t(Round {0}) ".format(r.get_id()) + Colours.ENDC + m.get_match_text())
                                                                matches_found = True
                                                    
                                                # No Matches Found
                                                if(not matches_found):
                                                    print(Colours.FAIL + "\tNo matches were found in this tournament." + Colours.ENDC)

                                        # Specific Tournament
                                        else:
                                            print()
                                            t = selected_tournament
                                            print("[{0}{1}{2}]:".format(Colours.OKBLUE, t.get_name(), Colours.ENDC))
                                            matches_found = False
                                            for r in t.get_rounds():
                                                mg = r.get_gender(self.genders[selected_gender-1])[1]

                                                if(not mg.is_complete()):
                                                    print(Colours.GRAY + "\t(Round {0} is incomplete, so data has not been pulled from here)".format(r.get_id()) + Colours.ENDC)
                                                else:
                                                    for m in mg.get_matches():
                                                        plyr_one = m.get_player_one()
                                                        plyr_two = m.get_player_two()

                                                        if((plyr_one[0] == plyr.get_name() and plyr_one[1] == scores[0] and plyr_two[1] == scores[1]) or (plyr_two[0] == plyr.get_name() and plyr_one[1] == scores[1] and plyr_two[1] == scores[0])):
                                                            print(Colours.GRAY + "\t(Round {0}) ".format(r.get_id()) + Colours.ENDC + m.get_match_text())
                                                            matches_found = True
                                                    
                                            # No Matches Found
                                            if(not matches_found):
                                                print(Colours.FAIL + "\tNo matches were found in this tournament." + Colours.ENDC)
                                        break
                                elif(selected_stat == 2):
                                    # All Tournaments
                                    if(type(selected_tournament) is str):
                                        print()
                                        for t in self.get_tournaments():
                                            round_wins = 0
                                            print("[{0}{1}{2}]:".format(Colours.OKBLUE, t.get_name(), Colours.ENDC))
                                            for r in t.get_rounds():
                                                mg = r.get_gender(self.genders[selected_gender-1])[1]

                                                if(not mg.is_complete()):
                                                    print(Colours.GRAY + "\t(Round {0} is {1}incomplete{2}, no data to pull here!)".format(r.get_id(), Colours.FAIL, Colours.GRAY) + Colours.ENDC)
                                                else:
                                                    print(Colours.GRAY + "\t(Round {0} is {1}complete{2}, data has been retrieved)".format(r.get_id(), Colours.OKGREEN, Colours.GRAY) + Colours.ENDC)
                                                    for m in mg.get_matches():
                                                        if(m.get_winner() == plyr.get_name()):
                                                            round_wins += 1
                                                
                                            print("\tThe percentage wins for {2}{0}{4} is: {3}{1}%{4} ({5}/{6})".format(plyr.get_name(), (round_wins / self.game.settings['round_count']) * 100, Colours.OKBLUE, Colours.OKGREEN, Colours.ENDC, round_wins, self.game.settings['round_count']))

                                    # Specific Tournament
                                    else:
                                        print()
                                        t = selected_tournament
                                        round_wins = 0
                                        
                                        print("[{0}{1}{2}]:".format(Colours.OKBLUE, t.get_name(), Colours.ENDC))
                                        for r in t.get_rounds():
                                            mg = r.get_gender(self.genders[selected_gender-1])[1]

                                            if(not mg.is_complete()):
                                                print(Colours.GRAY + "\t(Round {0} is {1}incomplete{2}, no data to pull here!)".format(r.get_id(), Colours.FAIL, Colours.GRAY) + Colours.ENDC)
                                            else:
                                                print(Colours.GRAY + "\t(Round {0} is {1}complete{2}, data has been retrieved)".format(r.get_id(), Colours.OKGREEN, Colours.GRAY) + Colours.ENDC)
                                                for m in mg.get_matches():
                                                    if(m.get_winner() == plyr.get_name()):
                                                        round_wins += 1

                                        print("\tThe percentage wins for {2}{0}{4} is: {3}{1}%{4} ({5}/{6})".format(plyr.get_name(), (round_wins / self.game.settings['round_count']) * 100, Colours.OKBLUE, Colours.OKGREEN, Colours.ENDC, round_wins, self.game.settings['round_count']))
                            else:
                                return self.statistical_analysis(True, selected_gender)
                        elif(selected_stat == 3 or selected_stat == 4):
                            # Wins
                            if(selected_stat == 3):
                                # All Tournaments
                                if(type(selected_tournament) is str):
                                    print()
                                    for p in self.get_players(self.genders[selected_gender-1]):
                                        print(p.get_name(), p.get_wins())
                                        ##TODO

                                # Specific Tournament
                                else:
                                    print()
                                    t = selected_tournament
                                    round_wins = 0
                                    
                                    print("[{0}{1}{2}]:".format(Colours.OKBLUE, t.get_name(), Colours.ENDC))
                                    for r in t.get_rounds():
                                        mg = r.get_gender(self.genders[selected_gender-1])[1]

                                        if(not mg.is_complete()):
                                            print(Colours.GRAY + "\t(Round {0} is {1}incomplete{2}, no data to pull here!)".format(r.get_id(), Colours.FAIL, Colours.GRAY) + Colours.ENDC)
                                        else:
                                            print(Colours.GRAY + "\t(Round {0} is {1}complete{2}, data has been retrieved)".format(r.get_id(), Colours.OKGREEN, Colours.GRAY) + Colours.ENDC)
                                            for m in mg.get_matches():
                                                if(m.get_winner() == plyr.get_name()):
                                                    round_wins += 1

                                    print("\tThe percentage wins for {2}{0}{4} is: {3}{1}%{4} ({5}/{6})".format(plyr.get_name(), (round_wins / self.game.settings['round_count']) * 100, Colours.OKBLUE, Colours.OKGREEN, Colours.ENDC, round_wins, self.game.settings['round_count']))
                            
                            # Losses
                            elif(selected_stat == 4):
                                # All Tournaments
                                if(type(selected_tournament) is str):
                                    print()
                                    for t in self.get_tournaments():
                                        round_wins = 0
                                        print("[{0}{1}{2}]:".format(Colours.OKBLUE, t.get_name(), Colours.ENDC))
                                        for r in t.get_rounds():
                                            mg = r.get_gender(self.genders[selected_gender-1])[1]

                                            if(not mg.is_complete()):
                                                print(Colours.GRAY + "\t(Round {0} is {1}incomplete{2}, no data to pull here!)".format(r.get_id(), Colours.FAIL, Colours.GRAY) + Colours.ENDC)
                                            else:
                                                print(Colours.GRAY + "\t(Round {0} is {1}complete{2}, data has been retrieved)".format(r.get_id(), Colours.OKGREEN, Colours.GRAY) + Colours.ENDC)
                                                for m in mg.get_matches():
                                                    if(m.get_winner() == plyr.get_name()):
                                                        round_wins += 1
                                            
                                        print("\tThe percentage wins for {2}{0}{4} is: {3}{1}%{4} ({5}/{6})".format(plyr.get_name(), (round_wins / self.game.settings['round_count']) * 100, Colours.OKBLUE, Colours.OKGREEN, Colours.ENDC, round_wins, self.game.settings['round_count']))

                                # Specific Tournament
                                else:
                                    print()
                                    t = selected_tournament
                                    round_wins = 0
                                    
                                    print("[{0}{1}{2}]:".format(Colours.OKBLUE, t.get_name(), Colours.ENDC))
                                    for r in t.get_rounds():
                                        mg = r.get_gender(self.genders[selected_gender-1])[1]

                                        if(not mg.is_complete()):
                                            print(Colours.GRAY + "\t(Round {0} is {1}incomplete{2}, no data to pull here!)".format(r.get_id(), Colours.FAIL, Colours.GRAY) + Colours.ENDC)
                                        else:
                                            print(Colours.GRAY + "\t(Round {0} is {1}complete{2}, data has been retrieved)".format(r.get_id(), Colours.OKGREEN, Colours.GRAY) + Colours.ENDC)
                                            for m in mg.get_matches():
                                                if(m.get_winner() == plyr.get_name()):
                                                    round_wins += 1

                                    print("\tThe percentage wins for {2}{0}{4} is: {3}{1}%{4} ({5}/{6})".format(plyr.get_name(), (round_wins / self.game.settings['round_count']) * 100, Colours.OKBLUE, Colours.OKGREEN, Colours.ENDC, round_wins, self.game.settings['round_count']))

                        input("\n>>> Press <Return> to continue...")
                        return self.statistical_analysis(False, selected_gender)
                    else:
                        if(selected_stat.lower() == "b"):
                            return self.statistical_analysis(False)
                        else:
                            return self.statistical_analysis(True, selected_gender)
                else:
                    if(selected_stat.lower() == "b"):
                        return self.statistical_analysis(False)
                    else:
                        return self.statistical_analysis(True, selected_gender)
            else:
                return self.statistical_analysis(True)
        else:
            if(selected_gender.lower() == "b"):
                return "SKIP"
            else:
                return self.statistical_analysis(True)
        """
        A - Number of wins for a player with a particular score
        B - The percentage wins of a player
        C - Show the player with most wins in the season
        D - Show the player with most loses in the season
        """
        pass

    def validate_season(self):
        # Validate Tournaments
        for t in self.get_tournaments():
            # Check Round Size
            if(len(t.get_rounds()) is not self.game.settings['round_count']):
                self.game.clear_screen()
                print("The Round Count of {0}, {1} is invalid! Round Limit: {2}, Round Count: {3}".format(self.get_name(), t.get_name(), self.game.settings['round_count'], len(t.get_rounds())))
                exit()
            
            # Validate Rounds
            for r in t.get_rounds():
                for g in r.get_genders():
                    # Validate Matches
                    for m in g[1].get_matches():
                        m.validate_match(self.game.settings['score_limit'][g[1].get_gender()], r.get_id())

            # Save Data
            self.save()

    def save(self):
        # Grab all data
        season_data = self.json_data

        for t in season_data["tournaments"]:
            tournament = season_data["tournaments"][t]
            for r in tournament:
                if(r != "rounds"):
                    continue

                rounds = tournament["rounds"]
                for _r in rounds:
                    _round = rounds[_r]
                    _round_id = int(_r[-1:])
                    for gender in _round:
                        _matches = [ ]
                        _count = 0
                        for m in _round[gender]:
                            _matches.append(self.get_tournament(t).get_round(_round_id).get_gender(gender)[1].get_matches()[_count].get_match_as_json())
                            _count += 1
                        season_data["tournaments"][t]["rounds"]["round_{0}".format(_round_id)][gender] = _matches

        # Save
        return File().update_season(self.get_name(), season_data)