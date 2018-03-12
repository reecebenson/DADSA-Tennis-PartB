# DADSA - Assignment 1
# Reece Benson

from functools import partial
from os import system as call
from classes.File import File
from classes.Menu import Builder
from classes.QuickSort import quick_sort as sort

class Tournament():
    _app = None
    _name = None
    _season = None
    _rounds = None
    _rounds_raw = None
    _prize_money = None
    _prize_money_unique = None
    _difficulty = None
    _file_saving = None

    def __init__(self, app, name):
        # Set our Application
        self._app = app

        # Set our variables
        self._name = name
        self._rounds = { }
        self._rounds_raw = { }
        self._file_saving = False

    def name(self):
        return self._name

    def file_saving(self):
        return self._file_saving

    def set_file_saving(self, value):
        self._file_saving = value
        return self.file_saving()

    def save_rounds(self):
        return File.update_tournament_rounds(self.season().name(), self.name(), self._rounds_raw)

    def toggle_file_saving(self, menu_ref):
        # Update State
        self._file_saving = not self._file_saving

        # Update File Settings
        File.update_file_saving(self.season().name(), self.name(), self.file_saving())

        # Update Round Data within 'seasons.json'
        if(self.file_saving()):
            self.save_rounds()
        
        # Update Menu item
        if(menu_ref != None):
            Builder.add_menu(menu_ref, "{0} Saving".format("Disable" if self.file_saving() else "Enable"), "{0}_{1}".format(menu_ref, "fs"))

        # Skip over monitor_input halt
        return "SKIP"

    def season(self):
        return self._season

    def set_season(self, season):
        self._season = season
        return self.season()

    def rounds(self):
        return self._rounds

    def round(self, gender, rnd_name):
        if(gender in self.rounds()):
            if(rnd_name in self.rounds()[gender]):
                return self.rounds()[gender][rnd_name]
            else:
                return None
        else:
            return None

    def add_round(self, gender, _round):
        if(not gender in self.rounds()):
            self._rounds[gender] = { }

        self._rounds[gender].update({ _round.name(): _round })
        return self._rounds[gender][_round.name()]

    def set_rounds(self):
        for rnd in self._rounds_raw:
            for gdr in self._rounds_raw[rnd]:
                # If the Gender category doesn't exist within the rounds, create it
                if(not gdr in self._rounds):
                    self._rounds[gdr] = [ ]

                # Populate our dictionary with our match data
                for match in self._rounds_raw[rnd][gdr]:
                    _round._matches.append(match)

                # Append our Round
                self._rounds[gdr].append(_round)

    def generate_round(self, gender, round_id, flag = None):
        # Generate specific round
        updated = self._app.handler.generate_round(self.season().name(), self.name(), round_id, gender)

        # Reload Menu
        if(updated and flag != "LOAD"):
            Builder.reload_menu()
            print("Successfully updated Round {0} for the {1} Gender on Tournament {2}.".format(round_id, gender.title(), self.name()))
        return None

    def input_round(self, gender, round_id, flag = None):
        # Generate specific round
        updated = self._app.handler.input_round(self.season().name(), self.name(), round_id, gender)

        # Reload Menu
        if(updated and flag != "LOAD"):
            Builder.reload_menu()
            print("Successfully inputted Round {0} for the {1} Gender on Tournament {2}.".format(round_id, gender.title(), self.name()))
        return None

    def edit_round(self, gender, round_id):
        # Check Round exists
        if(not self.round(gender, "round_{}".format(round_id))):
            return None

        # Header
        print("Editing {3} - {0} Round {1} - {2} matches exist\n".format(
                                                            gender.title(),
                                                            round_id,
                                                            len(self.round(gender, "round_{}".format(round_id)).matches()),
                                                            self.name()
                                                            ))

        # Count the changes made
        changes_made = 0

        for m in self.round(gender, "round_{}".format(round_id)).matches():
            shouldEdit = input("Would you like to edit [{1}] '{0}'? [y/N]: ".format(m.versuses(True), m.id())) or "n"

            if(shouldEdit.lower() == "y"):
                # Flag for changes in this match
                match_winner = m.winner()[0].name()
                match_changes = False
                match_cap = m.round().cap()

                # Player One Score
                plyr_one_score = input("Enter the Score for {0} (default: {1}): ".format(m.player_one()[0].name(), m.player_one()[1])) or str(m.player_one()[1])

                # Check if our score is different
                if(plyr_one_score.isdigit() and int(plyr_one_score) != m.player_one()[1]):
                    match_changes = True
                    changes_made += 1
                    m._player_one_score = int(plyr_one_score)

                # Player Two Score
                plyr_two_score = input("Enter the Score for {0} (default: {1}): ".format(m.player_two()[0].name(), m.player_two()[1])) or str(m.player_two()[1])
                if(plyr_two_score.isdigit() and int(plyr_two_score) != m.player_two()[1]):
                    match_changes = True
                    changes_made += 1
                    m._player_two_score = int(plyr_two_score)

                # Validate the match data
                m.validate()

                # Check if changes have been made
                if(match_changes):
                    # Check for winner change
                    if(match_winner != m.winner()[0].name()):
                        deleted_rounds = ", ".join([ r for r in self.rounds()[gender] if(self.round(gender, r).id() > round_id) ])
                        print("A new winner has been selected for this match, causing the deletion of the following rounds: {0}".format(deleted_rounds if deleted_rounds != "" else "< none >"))

                        # Delete rounds
                        for r in self.rounds()[gender].copy():
                            if(self.round(gender, r).id() > round_id):
                                # Update rounds_raw
                                self.delete_round(gender, r)
                    
                    # Update raw match data
                    self._rounds_raw["round_{}".format(round_id)][gender][m.id()].update({ m.player_one()[0].name(): m.player_one()[1], m.player_two()[0].name(): m.player_two()[1] })

                    # Save file
                    self.save_rounds()

                    # Debug
                    print("Match [{0}] has been updated successfully -> [{1}]\n".format(m.id(), m.versuses(True)))
                else:
                    print("No changes were made to Match [{0}] -> {0}\n".format(m.id(), m.versuses(True)))

        # Force a Menu Rebuild
        Builder.reload_menu()

        return None

    def clear_round(self, gender, round_id):
        # Verification
        verif = input("Are you sure you want to clear the following rounds [y/N]?\n{0}\n>>> ".format(", ".join([ r for r in self.rounds()[gender] if(self.round(gender, r).id() >= round_id) ]))) or "n"

        if(verif.lower() == "y"):
            # Delete rounds
            for r in self.rounds()[gender].copy():
                if(self.round(gender, r).id() >= round_id):
                    # Update rounds_raw
                    self.delete_round(gender, r)

                    # Output
                    print("Deleted Round: {0} -> {1} -> {2}".format(self.name(), gender, "Round "+str(r[-1:])))

            # Save file
            self.save_rounds()
        else:
            print("Cancelled ")

        # Force a Menu Rebuild
        Builder.reload_menu()
        return None

    def delete_round(self, g, r_id):
        # Check if our round exists
        if(not r_id in self._rounds_raw):
            return None

        # Check if our round gender exists
        if(not g in self._rounds_raw[r_id]):
            return None

        # Delete our round raw data
        self._rounds_raw[r_id].pop(g)

        # Update self variables
        self._rounds[g].pop(r_id)

        # Clean up
        if(len(self._rounds_raw[r_id]) == 0):
            self._rounds_raw.pop(r_id)

        # Done!
        return True

    def update_rounds_raw(self):
        # Import our data into JSON format for saving reference
        for g in self.rounds():
            for r_id, r in enumerate(self.rounds()[g], 1):
                # Make sure our round exists within the raw data
                if(not "round_{0}".format(r_id) in self._rounds_raw):
                    self._rounds_raw.update({ "round_{0}".format(r_id): { } })

                # Make sure our gender exists within the raw data
                if(not g in self._rounds_raw["round_{0}".format(r_id)]):
                    self._rounds_raw["round_{0}".format(r_id)].update({ g: [ ] })

                # Insert our data
                self._rounds_raw["round_{0}".format(r_id)][g] = [ { m.player_one()[0].name(): m.player_one()[1], m.player_two()[0].name(): m.player_two()[1] } for m in self.round(g, r).matches() ]
    
        return True

    def prize_money(self):
        return self._prize_money

    def set_prize_money(self, prize_money):
        self._prize_money = prize_money

    def difficulty(self):
        return self._difficulty

    def set_difficulty(self, difficulty):
        self._difficulty = difficulty

    def go_to_edit_round(self, gdr, r):
        # Define our Menu Tree
        _menu_tree = [  "main",
                        "load_season",
                        "ls_[{0}]".format(self.season().name()),
                        "ls_[{0}]_[{1}]".format(self.season().name(), self.name()),
                        "ls_[{0}]_[{1}]_rs".format(self.season().name(), self.name()),
                        "ls_[{0}]_[{1}]_rs_{2}".format(self.season().name(), self.name(), gdr),
                        "ls_[{0}]_[{1}]_vr_{2}_round_{3}_edit".format(self.season().name(), self.name(), gdr, r) ]
        _menu_current = _menu_tree[-1]

        # Set our Current Menu
        Builder._current = _menu_current
        Builder._tree = _menu_tree

        # Force close the emulation
        return "SKIP"

    def emulate(self, gdr):
        # Set some variables
        r = 0
        force_exit = False
        invalid_option = False

        # Start the emulation of our tournament
        while (r < self.season().settings()["{}_round_count".format(gdr)] and force_exit == False):
            # Forcing to exit the while?
            if(force_exit):
                break

            # Increment r
            r += 1

            # Get our round
            rnd = "round_{0}".format(r)

            # Clear Terminal
            call("cls")

            # Check if our round exists
            if(self.round(gdr, rnd)):
                # Print our round
                print("——————————————————————————————————————————————————————————————")
                print("Round {0} Results:".format(r))
                emulation = self.emulate_round(gdr, rnd, True)

                # Setup our options
                options = emulation[0]
                options_funcs = emulation[1]

                # Can we continue to another round?
                if(r != self.season().settings()["{}_round_count".format(gdr)]):
                    options = [ "Continue to the next round" ] + options
                    options_funcs = [ "continue" ] + options_funcs

                # Can we go back a round?
                if(r != 1):
                    options.append("Go back a round")
                    options_funcs.append("back")

                # Add our other options
                options.append("Edit this round")
                options_funcs.append(partial(self.go_to_edit_round, gdr, r))
                options.append("Stop Tournament Emulation")
                options_funcs.append("end")

                # Check if we had an error
                if(invalid_option):
                    print("\nError:\nYou entered an invalid option.")
                    invalid_option = False

                # Menu
                cur_index = 1
                print("\nPlease select an option:")

                # Print the options available to this round
                for opt in options:
                    print("{}.".format(cur_index), opt)
                    cur_index += 1

                option = input(">>> ")
                if(option.isdigit()):
                    option = int(option)

                    if(option > 0 and option < cur_index):
                        # Run function
                        func_to_run = options_funcs[option - 1]

                        if(callable(func_to_run)):
                            callback = func_to_run()

                            if(callback == "SKIP"):
                                force_exit = True
                            else:
                                r -= 1
                                invalid_option = False
                        else:
                            if(func_to_run == "back"):
                                r -= 2
                                invalid_option = False
                            elif(func_to_run == "end"):
                                r = self.season().settings()["{}_round_count".format(gdr)] + 1
                                force_exit = True
                            else:
                                pass
                    else:
                        r -= 1
                        invalid_option = True
                else:
                    r -= 1
                    invalid_option = True
            else:
                # Round does not exist
                break

        if(not force_exit):
            # Have we reached the end of our rounds?
            if(r == self.season().settings()["{}_round_count".format(gdr)]):
                print("End of Tournament {0}. 1st Place Winner: {1}".format(self.name(), self.rounds()[gdr]["round_{0}".format(r)].winners()[0].name()))
            else:
                # Did not reach the end of the tournament
                print("\nError:\nUnable to emulate {0} {1} Round {2} as it does not exist.\n".format(self.name(), gdr.title(), r))
                print("Please select an option:", "\n1.", "Modify this round", "\n2.", "Stop Tournament emulation")
                option = input(">>> ") or "2"
                if(option == "1"):
                    # Define our Menu Tree
                    _menu_tree = [  "main",
                                    "load_season",
                                    "ls_[{0}]".format(self.season().name()),
                                    "ls_[{0}]_[{1}]".format(self.season().name(), self.name()),
                                    "ls_[{0}]_[{1}]_rs".format(self.season().name(), self.name()),
                                    "ls_[{0}]_[{1}]_rs_{2}".format(self.season().name(), self.name(), gdr),
                                    "ls_[{0}]_[{1}]_vr_{2}_round_{3}".format(self.season().name(), self.name(), gdr, r) ]
                    _menu_current = _menu_tree[-1]

                    # Set our Current Menu
                    Builder._current = _menu_current
                    Builder._tree = _menu_tree

                    # Skip over the input handling from Menu Builder
                    return "SKIP"
                elif(option == "2"):
                    return None
                else:
                    return None
        else:
            return "SKIP"

    def emulate_round(self, gdr = None, rnd = None, all = False, error = False):
        # Clear Terminal
        call("cls")

        # Get our Matches
        for m, match in enumerate(self.round(gdr, rnd).matches(), 1):
            print(match.versuses(True))

        # Options
        if(all):
            return ([ "View current leaderboard", "View current prize money" ], [ partial(self.view_leaderboard, gdr, rnd), partial(self.view_prize_money, gdr) ]) if(rnd == "round_{}".format(self.season().settings()["round_count"])) else ([ "View current leaderboard" ], [ partial(self.view_leaderboard, gdr, rnd) ])
        else:
            # Have we errored?
            if(error):
                print("\nError:\nYou entered an invalid option.")
                error = False

            # Are we on our last round?
            if(rnd == "round_{}".format(self.season().settings()["round_count"])):
                # Build Menu
                print("\nPlease select an option:", "\n1.", "View current leaderboard", "\n2.", "View current prize money", "\n3.", "Back to menu")
                option = input(">>> ") or None

                if(option == "1"):
                    self.view_leaderboard(gdr, rnd)
                elif(option == "2" and rnd == "round_{}".format(self.season().settings()["round_count"])):
                    self.view_prize_money(gdr)
                elif(option == "3"):
                    return "SKIP"
                else:
                    return self.emulate_round(gdr, rnd, all, True)
            else:
                # Build Menu
                print("\nPlease select an option:", "\n1.", "View current leaderboard", "\n2.", "Back to menu")
                option = input(">>> ") or None

                if(option == "1"):
                    self.view_leaderboard(gdr, rnd)
                elif(option == "2"):
                    return "SKIP"
                else:
                    return self.emulate_round(gdr, rnd, all, True)
            
            # Repeat our Round
            return self.emulate_round(gdr, rnd, all)

    def view_leaderboard(self, gdr = None, rnd_name = None):
        # Get our Round Object
        rnd = self.round(gdr, rnd_name)

        # Clear our Terminal
        call("cls")
        
        # Set our header text
        print("View Leaderboard for '{0}', Round {1}:".format(self.name(), rnd.id()))
        print("—————————————————————————————————————————————————————————")

        srt = sort(self.season().players()[gdr], self.name())
        place = 1
        for i in reversed(range(len(srt))):
            print("#{0}: {1} — {2} — {3}".format(f"{place:02}", srt[i].name(), "{0:03d} score".format(srt[i].score(self.name(), rnd_name) if (srt[i].score(self.name(), rnd_name) != 0) else srt[i].highest_score(self.name(), False)), "{0:03d} diff score".format(int(srt[i].score(self.name(), rnd_name) * self.difficulty()) if (srt[i].score(self.name(), rnd_name) != 0) else int(srt[i].highest_score(self.name(), False) * self.difficulty()))))
            place += 1
        
        # Hold User
        input(">>> Press <Return> to continue...")

    # Used to define the players new ranking points and can be used to organise the top 16 players
    def unique_prize_money(self):
        # Organise a unique list if it hasn't already been sorted
        if(self._prize_money_unique == None):
            # Remove duplicates
            self._prize_money_unique = []
            [ self._prize_money_unique.append(i) for i in self._prize_money if not self._prize_money_unique.count(i) ]

            # Fix some shit
            while(len(self._prize_money_unique) <= self.season().settings()["round_count"]):
                self._prize_money_unique.append(0)

            # Reverse our list
            self._prize_money_unique.reverse()

        # Return a reversed list
        return self._prize_money_unique

    def view_prize_money(self, gdr = None):
        # Clear our Terminal
        call("cls")

        # Get our unique prize money thingies
        self.unique_prize_money()

        # Set our header text
        print("View Prize Money for '{0}':".format(self.name()))
        print("—————————————————————————————————————————————————————————")

        srt = sort(self.season().players()[gdr], self.name())
        place = 1
        for i in reversed(range(len(srt))):
            # Get the players Prize Money
            p_prizemoney = self._prize_money_unique[srt[i].wins(self.name())]
                
            # Print Data
            print("#{0}: {1} — £{2:,}".format(f"{place:02}", srt[i].name(), p_prizemoney))
            place += 1
        
        # Hold User
        input(">>> Press <Return> to continue...")

    def display(self, detail, extra = None):
        # Set our header text
        ret = "Details about '{0}':".format(self.name()) + "\n"
        ret += "—————————————————————————————————————————————————————————" + "\n"
        
        # What detail are we handling?
        if(detail == "difficulty"):
            # Add difficulty string to the return string
            ret += "The difficulty multiplier for this tournament has been set as: {0}".format(self.difficulty()) + "\n"
        elif(detail == "prize_money"):
            ret += "Prize Money:" + "\n"
            ret += "{0}".format("\n".join([ "  #{0}: £{1:,}".format(i, int(t)) for i, t in enumerate(self.prize_money(), 1) ])) + "\n"
        else:
            ret = "An unknown error has been handled..."
        return ret