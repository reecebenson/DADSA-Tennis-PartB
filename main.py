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
        builder = Builder().init(self.game, False)
        builder.add_menu("main", "Start a new session", "new_session")
        builder.add_menu("main", "Load previous session", "previous_session")
        builder.add_func("main", "new_session", partial(self.new_session, builder))
        builder.add_func("main", "previous_session", partial(self.previous_session, builder))

        # Show menu
        builder.show_current_menu()

        ###############################################################################

        # Load our Game
        self.game.load(self.loading_mode)

        # Load our Menu
        self.menu = Menu.Menu(self.game)
        self.menu.load()

        # Hold the program
        self.exit()

    # Loading Mode - New Session
    def new_session(self, b):
        print("Starting a new session will remove all previous data.")
        resp = input("Are you sure you would like to start a new session? [y/N]: ")
        if(resp.lower() == "y"):
            self.loading_mode = "new"
            b.close_menu()
        elif(resp.lower() == "n"):
            pass
        return "SKIP"

    # Loading Mode - Previous Session
    def previous_session(self, b):
        self.loading_mode = "previous"
        b.close_menu()
        return "SKIP"

    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input("\n>>> Press <Return> to terminate the program")
        sys.exit()

App()