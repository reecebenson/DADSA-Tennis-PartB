"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
# Imports
import csv

# Variables
limit = 3
csvPath = "../data/csv/"
nameTemplate = "DADSA 1718 COURSEWORKB TBS2 ROUND"

# Loop through CSV files
for i in range(1, 6):
    name = "{0} {1} {2}.csv".format(nameTemplate, i, "MEN")
    path = "{0}{1}".format(csvPath, name)

    print("{0}{1}".format(path, "\n"))
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=",")

        for i, line in enumerate(reader):
            if(i == 0):
                continue

            playerOne = line[0]
            scoreOne = int(line[1])
            playerTwo = line[2]
            scoreTwo = int(line[3])

            winnerName = playerOne if scoreOne > scoreTwo else playerTwo

            if scoreOne == scoreTwo:
                winnerName = ""

            yay = False
            if scoreOne == limit:
                yay = True
            
            if scoreTwo == limit:
                yay = True

            if not yay:
                winnerName = "injury"

            if scoreOne == limit and scoreTwo == limit:
                winnerName = "dupe"

            if scoreOne > limit or scoreTwo > limit:
                winnerName = "limit exceeded"

            print("{{\"{0}\": {1}, \"{2}\": {3}, \"winner\": \"{4}\"}},".format(playerOne, scoreOne, playerTwo, scoreTwo, winnerName))