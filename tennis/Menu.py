"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
import traceback
from functools import partial
from os import system as call
from collections import OrderedDict

class Menu():
    # Define our Game
    game = None

    def __init__(self, _game):
        self.game = _game

    def load(self, reloading = False):
        # Temporary Menu Debug
        menu_debug = True

        # Create our Menu
        builder = Builder().init(self.game, False, reloading)

        ## MAIN ------------------------------------------------------------------------------------------------------------------------------
        builder.add_menu("main", "Load Game", "loadgame")
        builder.add_info("loadgame", "List the seasons within this Tennis game.")
        builder.add_menu("main", "Developer Information", "info")
        builder.add_info("info", "Show information about the developer.")
        if(menu_debug): builder.add_menu("main", "Debugging", "debug")
        builder.add_func("main", "info", partial(print, "Created by Reece Benson, 16021424."))

        ## SEASONS ---------------------------------------------------------------------------------------------------------------------------
        for season in self.game.seasons:
            season_obj = self.game.seasons[season]
            season_id = season[-1:]
            builder.add_menu("loadgame", "Season {}".format(season_id), "view_{}".format(season))

            ## DEBUG -------------------------------------------------------------------------------------------------------------------------
            if(menu_debug):
                builder.add_menu("debug", "List Season {} Players".format(season_id), "debug_list_players_s{}".format(season_id))
                builder.add_func("debug", "debug_list_players_s{}".format(season_id), partial(season_obj.list_players))

            ## TOURNAMENTS -------------------------------------------------------------------------------------------------------------------
            for tournament in self.game.seasons[season].get_tournaments():
                builder.add_menu("view_{}".format(season), tournament.get_name(), "t{}".format(tournament.get_name()))

                ## ROUNDS --------------------------------------------------------------------------------------------------------------------
                for t_round in tournament.get_rounds():
                    builder.add_menu("t{}".format(tournament.get_name()), "Round {}".format(t_round.get_id()), "t{}_r{}".format(tournament.get_name(), t_round.get_id()))

                    ## GENDERS ---------------------------------------------------------------------------------------------------------------
                    for gdr in t_round.get_genders():
                        builder.add_menu("t{}_r{}".format(tournament.get_name(), t_round.get_id()), gdr.title(), "t{}_r{}_g{}".format(tournament.get_name(), t_round.get_id(), gdr))

                        ## CHECK GENDER IS AVAILABLE
                        if(t_round.is_available(gdr)):
                            builder.add_func("t{}_r{}".format(tournament.get_name(), t_round.get_id()), "t{}_r{}_g{}".format(tournament.get_name(), t_round.get_id(), gdr), partial(t_round.run, gdr))
                            #builder.add_func("t{}_r{}".format(tournament.get_name(), t_round.get_id()), "t{}_r{}_g{}".format(tournament.get_name(), t_round.get_id(), gdr), partial(self.mark_as_available, season, tournament.get_name(), t_round.get_name(), gdr))

        # Show Menu
        builder.show_current_menu()

    """def mark_as_available(self, season_name, tournament_name, round_name, gender):
        round_id = int(round_name[-1:])

        season = self.game.get_season(season_name)
        tournament = season.get_tournament(tournament_name)
        t_round = tournament.get_round(round_id + 1)
        t_round.set_available(gender)
        print("Set Season {}, Tour {}, Round {} for {} as available.".format(season_name, tournament_name, round_id, gender))
        self().reload_menu()"""


"""Start of Menu self Class"""        
class Builder():
    game = None
    _menu = None
    _tree = None
    _current = None
    _title = None
    _force_close = None
    _force_reload = None
    _submenu = None

    def init(self, game, title = False, reloading = False, submenu = False):
        # Set our variables
        self.game = game
        self._menu = { }
        self._submenu = submenu

        # Flags will be reset when the menu is closed and reinitialised, or when the menu is closed and then reloaded (init called again)
        self._force_close = False
        self._force_reload = False

        # If we're reloading, don't reset our current pos or data related to current open menu
        if(not reloading):
            # Set our other variables
            self._tree = [ "main" ]
            self._current = "main"
            self._title = "Please select an option:" if not title else title

        # Return Object
        return self

    def close_menu(self):
        # Set our flag
        self._force_close = True

    def reload_menu(self):
        # We will pop() [go back] to avoid hitting any errors (maybe menu is replaced with a function, etc)
        #self.go_back(True)

        # Set our flag
        self._force_reload = True

    def add_menu(self, menu, name, ref):
        # Check if this submenu exists
        if(not menu in self._menu):
            self._menu[menu] = { }

        # Update our Menu
        self._menu[menu].update({ ref: name })

    def add_info(self, ref, info):
        # Add additional information to a menu item
        self._menu[ref+"_info"] = info

    def add_func(self, name, ref, func):
        # Add a selectable function to the referred menu item
        self._menu[ref] = func

    def get_item(self, ref):
        # Get an existing item, otherwise return None
        if(not ref in self._menu):
            return None
        else:
            return self._menu[ref]
        return None

    def call_func(self, ref):
        # Call the function reference of a menu item
        if(self.is_func(ref)):
            return self.get_item(ref)()
        else:
            return None

    def is_func(self, ref):
        # Check if the function reference is callable / is a function
        return callable(self.get_item(ref))

    def item_exists(self, ref):
        # Check if a menu item or reference exists
        return (ref in self._menu)

    def is_menu(self, ref):
        # Set flag
        is_a_menu = True
        
        # Check if the "menu" exists
        if(not ref in self._menu):
            is_a_menu = False

        # Check if the menu is a dictionary
        if(type(self.get_item(ref)) != dict):
            is_a_menu = False

        return is_a_menu

    def notAvailable(self, text):
        # Append a string as a suffix
        return text + " (Not Available)"

    def find_menu(self, index):
        # Get our current menu to check the items for
        cur_menu_items = self.get_item(self.current_menu())

        # Check that our menu exists
        if(cur_menu_items == None):
            print("There was an error with grabbing the selected menu!")
            self.set_current_menu("main")
            return False
        else:
            # Iterate through our items to find our index
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                if(index == i):
                    return { "menu": self.is_menu(k), "ref": k, "name": v }

            # Return Data
            return False

        # Fall back returning statement
        return False

    def show(self):
        # Print a tree of the current built menu
        print(self._menu)

    def current_menu(self):
        # Return the current menu (top of the stack)
        return self._current

    def set_current_menu(self, new_menu):
        # Set the current menu
        self._current = new_menu
        return self.current_menu()

    def add_menu_tree(self, ref):
        # Add to our current menu tree
        self._tree.append(ref)

    def get_menu_tree(self):
        # Get our current menu tree as a string, split by forward slash (/)
        return "/".join([ m for m in self._tree ])

    def go_back(self, reloading = False):
        # Set our flag to true
        self.just_called_back = True

        # Pop off the last item of the list
        self._tree.pop()

        # Set our current menu to the last element of the list
        self._current = self._tree[-1]

        # Display our menu
        if(not reloading):
            return self.show_current_menu()

        return None

    def monitor_input(self):
        # Check if we're force closing the menu or if we're reloading the menu
        if(self._force_close):
            return

        try:
            # Validate our input
            resp = input("\n>>> ")

            # Validate response
            if(resp.lower() == "exit" or resp.lower() == "quit" or resp.lower() == "x"):
                # Terminate the program after user confirmation
                raise KeyboardInterrupt
            elif(resp == ""):
                # Invalid Input from User
                return self.show_current_menu(True, True, "You have entered an invalid option")

            # Check that the menu option exists
            try:
                # See if we're trying to go back a page
                if(resp.lower() == "b" and self._current is not "main"):
                    return self.go_back()

                # Convert our request to an integer
                req = int(resp)

                # Find the requested menu
                req_menu = self.find_menu(req)
                if(type(req_menu) == dict):
                    if(req_menu['menu']):
                        # Display our menu
                        self.set_current_menu(req_menu['ref'])
                        self.add_menu_tree(req_menu['ref'])
                        self.show_current_menu()
                    else:
                        # Double check we're executing a function
                        if(self.is_func(req_menu['ref'])):
                            # Clear Terminal
                            call("cls")

                            # Print Function Header
                            if(self.game.debug):
                                print(" _______ ______ _   _ _   _ _____  _____ ")
                                print("|__   __|  ____| \\ | | \\ | |_   _|/ ____|")
                                print("   | |  | |__  |  \\| |  \\| | | | | (___  ")
                                print("   | |  |  __| | . ` | . ` | | |  \\___ \\ ")
                                print("   | |  | |____| |\\  | |\\  |_| |_ ____) |")
                                print("   |_|  |______|_| \\_|_| \\_|_____|_____/ ")
                            print("——————————————————————————————————————————————————————————————")

                            # Execute
                            retStr = self.call_func(req_menu['ref'])

                            # Hold user (to display output from function)
                            if(retStr != "SKIP"):
                                input("\n>>> Press <Return> to continue...")

                            if(not self._force_reload):
                                return self.show_current_menu()
                            else:
                                self.game.menu = Menu(self.game)
                                return self.game.menu.load(True)
                        else:
                            if(not self.item_exists(req_menu['ref'])):
                                return self.show_current_menu(True, True, "That option is unavailable")
                            else:
                                if(req_menu['ref'] == "return"):
                                    # User wants to go back to the default menu
                                    input("\nYou are now going to the main menu!\nWarning: If data has not been added, rounds will not exist!")
                else:
                    # Check if we pressed the Back button
                    current_menu = self.get_item(self._current)
                    if(req == (len(current_menu) + 1) and self._current is not "main"):
                        return self.go_back()
                    elif(req == (len(current_menu) + 1) and self._current is "main"):
                        return self.game.exit() if not self._submenu else None 
                    else:
                        return self.show_current_menu(True, True, "You have entered an invalid option")
            # Exceptions (handled from outer-scope try/except)
            except KeyboardInterrupt:   raise KeyboardInterrupt
            except ValueError:          raise ValueError
            except Exception:           raise Exception

        # Exceptions
        except KeyboardInterrupt:
            # User has terminated the program (Ctrl+C)
            return self.game.exit() if not self._submenu else None
        except ValueError:
            # User has entered an invalid value
            return self.show_current_menu(True, True, "You have entered an invalid option")
        except Exception:
            # Handle other exceptions, and if debugging - show the error and halt the application
            if(self.game.debug):
                print("\nERROR:\nError Handled:\n{0}\n".format(traceback.print_exc()))
                input("...continue")
            # Application has handled error for User
            return self.show_current_menu(True, True)

    def show_current_menu(self, shouldClear = True, error = False, errorMsg = None):
        cur_menu_items = self.get_item(self.current_menu())

        # Should we clear our terminal window?
        if(shouldClear):
            call("cls")

        # Have we got an error?
        if(error):
            if(errorMsg == None):
                print("\nError:\nThere was an error performing your request.\n")
            else:
                print("\nError:\n{0}.\n".format(errorMsg))

        # Check that our Menu exists
        if(cur_menu_items == None):
            print("There was an error with grabbing the selected menu!")
            print("Current menu: {}".format(self.current_menu()))
            self.set_current_menu("main")
        else:
            # Print menu header
            print("{0} ({1})".format(self._title, self.get_menu_tree()))
            
            # Print out our menu
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                if(self.item_exists(k)):
                    print("{0}. {1}{2}".format(i, v, (' -> ' if self.is_menu(k) else '')))
                else:
                    print(self.notAvailable("{0}. {1}{2}".format(i, v, (' -> ' if self.is_menu(k) else ''))))

                # Does this key (ref) have info?
                if(self.item_exists(k+"_info")):
                    print("   - {0}{1}".format(self.get_item(k+"_info"), "" if (i == len(cur_menu_items.items()) and self.current_menu() is "main") else "\n"))

            # Print our back button
            if(self.current_menu() is not "main"):
                print("b. Back")
            else:
                print("x. Exit and Save" if not self._submenu else "x. Exit back to Main Menu") 

            # Get input from user
            self.monitor_input()
