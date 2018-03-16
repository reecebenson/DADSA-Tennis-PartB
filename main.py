"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
# Imports
import traceback
import sys
from tennis import Game
from tennis import Menu
from functools import partial
from tennis.Menu import Builder

class App():
    # Define the variables we will be using
    menu = None
    game = None
    loading_mode = None

    # Define all of the properties we will need to use
    def __init__(self):
        # Initialise our Game
        self.game = Game.Game(self)

        # Loading Mode
        Builder().init(self.game, False)
        Builder().add_menu("main", "\x1B[3mStart a new session", "new_session")
        Builder().add_menu("main", "Load previous session", "previous_session")
        Builder().add_func("main", "new_session", partial(self.new_session))
        Builder().add_func("main", "previous_session", partial(self.previous_session))

        # Show menu
        Builder().show_current_menu()

        ###############################################################################

        # Load our Game
        self.game.load(self.loading_mode)

        # Load our Menu
        self.menu = Menu.Menu(self.game)
        self.menu.load()

        # Hold the program
        self.exit()

    # Loading Mode - New Session
    def new_session(self):
        print("Starting a new session will remove all previous data.")
        resp = input("Are you sure you would like to start a new session? [y/N]: ")
        if(resp.lower() == "y"):
            self.loading_mode = "new"
            Builder().close_menu()
        elif(resp.lower() == "n"):
            pass
        return "SKIP"

    # Loading Mode - Previous Session
    def previous_session(self):
        self.loading_mode = "previous"
        Builder().close_menu()
        return "SKIP"

    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input("\n>>> Press <Return> to terminate the program")
        sys.exit()

App()