"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
from tennis import Match
from tennis.Menu import Menu
from tennis.Menu import Builder
from tennis.Colours import Colours
from tools.QuickSort import quick_sort_score as QuickSort
from functools import partial

class MatchGender():
    # Variables
    game = None
    gender = None
    parent = None
    matches = None
    available = None
    complete = None
    input_file_state = None
    pop_player_list = None

    # End of Round Variables
    complete_scores = None

    def __init__(self, _game, _gender, _parent):
        # Set Variables
        self.game = _game
        self.gender = _gender
        self.parent = _parent
        self.matches = [ ]
        
        # Set Flags
        self.pop_player_list = None
        self.available = False
        self.complete = False
        self.input_file_state = True if self.parent.parent.parent.get_id() == 1 else False

        # End of Round Variables
        self.complete_scores = [ ]

    def add_match(self, match):
        m = Match.Match(self.game, self.gender, self, match)
        self.matches.append(m)
        return m

    def get_gender(self):
        return self.gender

    def is_complete(self):
        return self.complete

    def set_complete(self, state):
        self.complete = state

        # Finalise this round
        self.finalise()

        # Check if this tournament for this gender is complete
        all_complete = True
        for t_round in self.parent.parent.get_rounds():
            mg = t_round.get_gender(self.gender)[1]
            if(not mg.is_complete()):
                all_complete = False
                break

        # Increase the wins of each winning player
        for m in self.get_matches():
            if(m.get_winner() == m.player_one):
                m.player_one_object.increment_wins(self.parent.parent.get_name())
                m.player_two_object.increment_losts(self.parent.parent.get_name())
            elif(m.get_winner() == m.player_two):
                m.player_two_object.increment_wins(self.parent.parent.get_name())
                m.player_one_object.increment_losts(self.parent.parent.get_name())

        # Are all the rounds complete?
        if(all_complete):
            # Mark Tournmanent as complete if both genders are valid
            for gender in self.parent.genders:
                completely_complete = True
                for t_round in self.parent.parent.get_rounds():
                    mg = t_round.get_gender(gender)[1]
                    if(not mg.is_complete()):
                        completely_complete = False
                        break
            
            # ALL
            if(completely_complete):
                self.parent.parent.set_complete(True)
                Builder().reload_menu()
        else:
            print("Not everything is complete.")

    def is_available(self):
        return self.available

    def set_availability(self, state):
        self.available = state

    def is_input_file_allowed(self):
        return self.input_file_state

    def set_input_file_state(self, state):
        self.input_file_state = state

    def get_matches(self):
        return [ m for m in self.matches ]

    def get_players(self):
        players = [ ]
        for m in self.get_matches():
            players.append(m.player_one)
            players.append(m.player_two)
        return players

    def get_players_objects(self):
        players = [ ]
        for m in self.get_matches():
            players.append(m.player_one_obj)
            players.append(m.player_two_obj)
        return players

    def get_winners(self):
        return [ m.get_winner() for m in self.get_matches() ]

    def set_next_round_as_available(self):
        # Mark next round as available
        next_round_id = self.parent.get_id() + 1
        if(next_round_id <= self.game.settings['round_count']):
            self.parent.parent.get_round(next_round_id).get_gender(self.gender)[1].set_availability(True)

            if(self.game.debug):
                print("\nSet Season {}, Tour {}, Round {} for {} as available.".format(self.parent.parent.parent.get_name(), self.parent.parent.get_name(), next_round_id, self.gender))
        
            return True
        return False

    def finalise(self):
        # Finalising the match records the players scores, etc.
        print("Finalising match...")

        # Setup List
        self.complete_scores = [ ]

        # Get Differences for each set of ranking points
        ranking_points = [ int(p) for p in reversed(list(self.game.settings['ranking_points'].keys())) ]
        diffs = [ (next_p - p) for next_p, p in zip(ranking_points, [0] + ranking_points[:]) ]

        # Get Allocation Score
        score_to_add = diffs[self.parent.get_id() - 1]

        # Get Previous Rounds Score
        previous_players = [ ]
        if(self.parent.get_id() > 1 and self.parent.get_id() <= self.game.settings["round_count"]):
            prev_round = self.parent.parent.get_round(self.parent.get_id() - 1).get_gender(self.gender)[1]
            if(len(prev_round.complete_scores) > 0):
                previous_players = prev_round.complete_scores

        for match in self.get_matches():
            # Bonus
            bonuses = match.get_match_bonuses()
            bonus = bonuses[0] if bonuses is not None else 1
            match_add_score = int(score_to_add)

            print("Winner: {}, score to set: {} ({})".format(match.get_winner(), match_add_score, "No Bonus" if bonus == 1 else "Bonus"))
            self.complete_scores.append((match.get_player_one()[0], match_add_score if match.get_winner() == match.get_player_one()[0] else 0, bonus))
            self.complete_scores.append((match.get_player_two()[0], match_add_score if match.get_winner() == match.get_player_two()[0] else 0, bonus))
        pass

    def run(self, error=False):
        # Clear Screen
        self.game.clear_screen()

        # Show Error
        if(error):
            print("\n" + Colours.BOLD + "Error:" + Colours.ENDC + "\n" + Colours.FAIL + "You have entered an invalid option.\n" + Colours.ENDC)

        # Menu Options
        print(Colours.BOLD + "Please select an option:" + Colours.ENDC + " (Viewing: " + "{3}{0}, Round {1}, {2}{4}".format(self.parent.parent.get_name(), str(self.parent.get_id()), self.get_gender().title(), Colours.GRAY, Colours.ENDC) + ")")
        print(Colours.OKGREEN + "1" + Colours.ENDC + ". View Round{}".format("" if self.is_complete() else Colours.FAIL + " (Not Available)" + Colours.ENDC))
        print(Colours.OKGREEN + "2" + Colours.ENDC + ". View Prize Money{}".format("" if self.is_complete() else Colours.FAIL + " (Not Available)" + Colours.ENDC))
        print(Colours.OKGREEN + "3" + Colours.ENDC + ". View Ranking Points{}".format("" if self.is_complete() else Colours.FAIL + " (Not Available)" + Colours.ENDC))
        print(Colours.OKGREEN + "4" + Colours.ENDC + ". Input using file data{}".format("" if (self.is_input_file_allowed() and not self.is_complete()) else Colours.FAIL + " (Not Available)" + Colours.ENDC))
        print(Colours.OKGREEN + "5" + Colours.ENDC + ". Input data manually{}".format("" if not self.is_complete() else Colours.FAIL + " (Not Available)" + Colours.ENDC))
        print(Colours.OKGREEN + "6" + Colours.ENDC + ". Go to Next Round{}".format("" if (not ((self.parent.get_id() + 1) > self.game.settings["round_count"]) and self.parent.parent.get_round(self.parent.get_id() + 1).get_gender(self.gender)[1].is_available()) else Colours.FAIL + " (Not Available)" + Colours.ENDC))
        print(Colours.FAIL + "x" + Colours.ENDC + ". Save and Return")

        # Menu Response
        resp = input(">>> ")
        if(resp.isdigit()):
            if(resp == "1"):
                if(self.is_complete()):
                    self.view()
                else:
                    self.run(True)
            elif(resp == "2"):
                if(self.is_complete()):
                    self.view_prize_money()
                else:
                    self.run(True)
            elif(resp == "3"):
                if(self.is_complete()):
                    self.view_ranking_points()
                else:
                    self.run(True)
            elif(resp == "4"):
                if(self.is_input_file_allowed() and not self.is_complete()):
                    self.input_file()
                else:
                    self.run(True)
            elif(resp == "5"):
                if(not self.is_complete()):
                    self.input_manual()
                else:
                    self.run(True)
            elif(resp == "6"):
                if(not ((self.parent.get_id() + 1) > self.game.settings["round_count"])):
                    if(self.parent.parent.get_round(self.parent.get_id() + 1).get_gender(self.gender)[1].is_available()):
                        return self.parent.parent.get_round(self.parent.get_id() + 1).get_gender(self.gender)[1].run()
                    else:
                        self.run(True)
                else:
                    self.run(True)
            else:
                return self.run(True)
        elif(resp == "x" or resp == "b"):
            self.game.save()
            Builder().go_back(True)
            Builder().reload_menu()
            return "SKIP"
        else:
            return self.run(True)

        # Recursive Menu
        return self.run()

    def view(self):
        # Clear Screen
        self.game.clear_screen()

        # Validate Matches
        for match in self.get_matches():
            match.validate_match(self.game.settings["score_limit"][self.gender], self.parent.get_id(), True)

        # Print Matches
        print("Viewing Matches for Season {0}, Tournament {1}, Round {2} of {3}s...".format(self.parent.parent.parent.get_id(), self.parent.parent.get_name(), self.parent.get_id(), self.get_gender()))
        for match in self.get_matches():
            print(match.get_match_text())
            match.get_match_bonuses_text()

        # Return
        input("\n>>> Press <Return> to continue...")

    def view_prize_money(self):
        # Temporary Player Scores
        player_scores = [ ]

        # Clear Screen
        self.game.clear_screen()

        # Go through each completed round
        for t_round in self.parent.parent.get_rounds():
            # Get Round Data
            mg = t_round.get_gender(self.gender)[1]

            # Break if Round is incomplete
            if(not mg.is_complete()):
                break

            # Set the scores
            for player_score in mg.complete_scores:
                player = player_score[0]
                score = float(player_score[1])

                # Find Player
                player_found = False
                i = 0
                for p in player_scores:
                    if(p['player'].get_name() == player):
                        player_scores[i] = { "score": p['score'] + score, "player": self.parent.parent.parent.get_player(player, self.gender) }
                        player_found = True
                    i += 1

                # Add Player
                if(not player_found):
                    player_scores.append({ "score": score, "player": self.parent.parent.parent.get_player(player, self.gender) })

        # Title
        print("Viewing Ranking Points for Season {0}, Tournament {1}, Round {2} of {3}s...".format(self.parent.parent.parent.get_id(), self.parent.parent.get_name(), self.parent.get_id(), self.get_gender()))
        overall_place = 1
        in_order = QuickSort(player_scores)
        for p in reversed(in_order):
            # Variables
            player = p['player']
            score = p['score']

            # Print Data
            print("#{0}: {1} — Prize Money: {2:002.2f}".format(f"{overall_place:02}", player.get_name(), self.parent.parent.prize_money[str(overall_place)] if str(overall_place) in self.parent.parent.prize_money else 0))
            overall_place += 1

        input("\n>>> Press <Return> to continue...")
        pass
    
    def view_ranking_points(self):
        # Temporary List of Player Scores, being updated each time for each completed round
        player_scores = [ ]

        # Clear Screen
        self.game.clear_screen()

        # Go through each completed round
        for t_round in self.parent.parent.get_rounds():
            # Get Round Data
            mg = t_round.get_gender(self.gender)[1]

            # Break if Round is incomplete
            if(not mg.is_complete()):
                break

            # Set the scores
            for player_score in mg.complete_scores:
                player = player_score[0]
                score = float(player_score[1])
                bonus = float(player_score[2])

                # Find Player
                player_found = False
                i = 0
                for p in player_scores:
                    if(p['player'].get_name() == player):
                        player_scores[i] = { "score": p['score'] + (score * bonus), "player": self.parent.parent.parent.get_player(player, self.gender) }
                        player_found = True
                    i += 1

                # Add Player
                if(not player_found):
                    player_scores.append({ "score": (score * bonus), "player": self.parent.parent.parent.get_player(player, self.gender) })

            # End Round
            if(t_round.get_id() == self.game.settings['round_count']):
                i = 0
                for p in player_scores:
                    player_scores[i] = { "score": p['score'] * t_round.parent.get_difficulty(), "player": player_scores[i]['player'] }
                    i += 1

        # Title
        print("Viewing Ranking Points for Season {0}, Tournament {1}, Round {2} of {3}s...".format(self.parent.parent.parent.get_id(), self.parent.parent.get_name(), self.parent.get_id(), self.get_gender()))
        overall_place = 1
        in_order = QuickSort(player_scores)
        for p in reversed(in_order):
            # Variables
            player = p['player']
            score = p['score']

            # Print Data
            print("#{0}: {1} — Score: {2:002.2f}".format(f"{overall_place:02}", player.get_name(), score))
            overall_place += 1

        input("\n>>> Press <Return> to continue...")
        pass

    def input_file(self):
        # Validate Matches
        for match in self.get_matches():
            match.validate_match(self.game.settings["score_limit"][self.gender], self.parent.get_id(), True)

        # Clear Screen
        self.game.clear_screen()

        # Print Matches
        print("Inputting matches for Season {0}, Tournament {1}, Round {2} of {3}s...".format(self.parent.parent.parent.get_id(), self.parent.parent.get_name(), self.parent.get_id(), self.get_gender()))
        for match in self.get_matches():
            print(match.get_match_text())

        # Mark next round as available
        self.set_complete(True)
        self.set_next_round_as_available()

        # Go back on the Main Menu
        input(">>> Press <Return> to continue...")

    def input_manual(self):
        # Players
        if(self.pop_player_list is None):
            self.pop_player_list = self.get_players()
            self.inputted_matches = [ ]

        # Disable File Input
        self.set_input_file_state(False)

        # Print Instructions
        error = False
        while(len(self.pop_player_list) is not 0):
            # Clear Screen
            self.game.clear_screen()

            # Cache Player List
            cached_player_list = self.pop_player_list[:]

            # Print Previous Matches
            if(len(self.inputted_matches) > 0):
                print("Current matches created:")
                for m in self.inputted_matches:
                    print("[{0}] {1} - {2} [{3}]".format(m['player_one'], m['player_one_score'], m['player_two_score'], m['player_two']))
                print()

            # Print Player List
            c = 0
            print("Available Players to create for Round {}".format(self.parent.get_id()))
            for p in self.pop_player_list:
                print("[{0}-{2}] {3}{4}{2}".format(Colours.OKGREEN, f"{c:02}", Colours.ENDC, Colours.BOLD, p), end='{}'.format("\n" if (((c+1) % 4) == 0 or c+1 == len(self.pop_player_list)) else " "))
                c += 1

            # Has Errored
            if(error):
                print("\n{0}{1}Error:{2}\n{0}You have entered an invalid value, please refer to the format.{2}".format(Colours.FAIL, Colours.BOLD, Colours.ENDC))
                error = False

            # Ask for Player Names
            print("\nPlease enter 2 player names in the following format: \"MP01,MP15\":")
            resp = input(">>> ")
            player_names = resp.upper().replace(" ", "").split(",")

            # Pop Players Names from the list
            if(len(player_names) == 2 and (player_names[0] != player_names[1])):
                if(player_names[0] in self.pop_player_list):
                    self.pop_player_list.remove(player_names[0])
                else:
                    self.pop_player_list = cached_player_list
                    error = True
                    continue

                if(player_names[1] in self.pop_player_list):
                    self.pop_player_list.remove(player_names[1])
                else:
                    self.pop_player_list = cached_player_list
                    error = True
                    continue
            else:
                error = True
                continue

            # Ask for Player Scores
            print("\nPlease enter the scores for {} vs. {}: (Example: \"{}-0\")".format(player_names[0], player_names[1], self.game.settings["score_limit"][self.gender]))
            resp = input(">>> ")
            player_scores = resp.replace(" ", "").split("-")

            # Validate Scores as Integers/Digits
            player_one_score = None
            player_two_score = None
            if(len(player_scores) == 2):
                if(player_scores[0].isdigit()):
                    player_one_score = int(player_scores[0])

                if(player_scores[1].isdigit()):
                    player_two_score = int(player_scores[1])

                if(player_one_score is None or player_two_score is None):
                    self.pop_player_list = cached_player_list
                    error = True
                    continue
            else:
                self.pop_player_list = cached_player_list
                error = True
                continue

            # Add match to temporary match list
            self.inputted_matches.append({ 'player_one': player_names[0], 'player_two': player_names[1], 'player_one_score': player_one_score, 'player_two_score': player_two_score })
            input("\nMatch Created: [{}] {} - {} [{}], press <Return> to continue...".format(player_names[0], player_scores[0], player_scores[1], player_names[1]))

        if((len(self.pop_player_list) == 0) and (len(self.inputted_matches) == len(self.get_players()) / 2)):
            # Set Flags
            self.set_complete(True)
            self.set_next_round_as_available()

            # Set Manual Input for next rounds
            for t_round in self.parent.parent.get_rounds():
                if(t_round.get_id() > self.parent.get_id()):
                    match_gender = t_round.get_gender(self.gender)[1]
                    match_gender.set_input_file_state(False)

            # Clear our Matches
            self.matches = [ ]
            for m in self.inputted_matches:
                m = self.add_match({ m['player_one']: m['player_one_score'], m['player_two']: m['player_two_score'], "winner": 'unknown' })
                m.validate_match(self.game.settings['score_limit'][self.gender], self.parent.get_id(), True)

        input(Colours.OKGREEN + "\n>>> Press <Return> to continue..." + Colours.ENDC)
