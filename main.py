"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
# Imports
from tennis.Menu import Menu
from tennis.Game import Game

class App():
    # Variables
    debug = True
    menu = None
    game = None

    # Entry Point
    def __init__(self):
        # Load our handler
        self.game = Game(self)
        self.game.load()

        # Show Menu
        #self.menu = Menu(self)
        #self.menu.load()

        # Hold the program
        self.exit()

    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input("\n\n>>> Press <Return> to terminate the program")
        exit()

App()