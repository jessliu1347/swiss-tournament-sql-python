Swiss Style Tournament Planner
==============================

Intro
=====
This project is a Python module backed by a PostgreSQL database to keep track of a Swiss Style Tournament.  Key functions include keeping track of player rankings (by number of wins/losses) and identifying the next round of player match-ups.  This application currently only supports one tournament at a time and an even number of players.

Set-up
======
Requires PostgreSQL and Python.  In the psql Command Line Interface, first run psql followed by \i tournament.sql import this file to set up the database.  Then run python your_client_program.py to run any Python program which calls the functions in tournament.py. 

Reference
=========
This module includes the following functions:
  * connect() - connects to the PostgreSQL database "tournament", returns a connection
  * deleteMatches() - removes all match records from the database
  * deletePlayers() - removes all player records from the database
  * countPlayers() - returns the number of players currently registered in the database
  * registerPlayer(name) - adds a player to the tournament database, input must be a string
  * playerStandings() - returns a list of tuples (id, name, wins, matches) showing players and their win records, sorted by number of wins descending
  * reportMatch(winner, loser) - records the outcome of a single match between two players, inputs are the id numbers of the winner and loser, respectively
  * swissPairings() - returns a list of tuples indicating the pairs of players (id1, name1, id2, name2) for the next round of a match
  * newTournament() - starts new tournament by removing all player and match records from the database

Author
======
Jessica Liu
