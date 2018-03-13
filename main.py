# DADSA - Assignment 1
# Reece Benson

import traceback
from tennis import Game
from tennis import Menu

class App():
    # Define the variables we will be using
    debug = False
    menu = None
    game = None

    # Define all of the properties we will need to use
    def __init__(self):
        # Load our Game
        self.game = Game.Game(self)
        self.game.load()

        # Load our Menu
        #self.menu = Menu.Menu(self)
        #self.menu.load()

        # Hold the program
        self.exit()

    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input("\n\n>>> Press <Return> to terminate the program")
        exit()

App()