FileHandler.py
    Manages all data files.
    Requests new data, appends to exisiting files, and tracks info about all existing files.
    Can be used to request information.

Data/info_table.json
    Tracks the inforamtion about all exisiting files.
    Its state is managed by FileHandler.
    Is essentially a python dictionary where each file id is a key and another dictionary containing information about the file is the value.
    The info is essentially what team in home, what team is away, what sport (directory the file is in), and what time the game starts.

Data/
    This directory holds directories for each sport, which contain files for each individual game.
    info_table.json also exists in this directory

Data/{sport}/{file_id}_h2h.csv
    Files contain the moneyline values for each game from each book in 10 minute increments

Data/{sport}/{file_id}_spreads.csv
    Files contain the spread values and prices for each game from each book in 10 minute increments

Data/{sport}/{file_id}_totals.csv
    Files contain the total value and prices for each game from each book in 10 minute increments