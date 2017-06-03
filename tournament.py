#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error: connection failed")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query = "truncate table matches cascade;"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "truncate table players cascade;"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "select count(player_id) from players;"
    cursor.execute(query)
    results = cursor.fetchone()
    num_players = results[0]
    db.close()
    return num_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "insert into players(name) values (%s);"
    parameter = (name,)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    query = "select players.player_id as id, players.name as name, " \
            "winners.wins as wins, num_matches.num_match as matches from (" \
            "players join winners on players.player_id = winners.player_id) " \
            "join num_matches on winners.player_id = num_matches.player_id " \
            "order by wins desc;"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "insert into matches(winner, loser) values (%s, %s);"
    parameters = (winner, loser)
    cursor.execute(query, parameters)
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, cursor = connect()
    query = "select rw1.player_id as id1, rw1.name as name1, rw2.player_id " \
            "as id2, rw2.name as name2 from rw_withnames as rw1 join " \
            "rw_withnames as rw2 on (rw1.rank = rw2.rank and rw1.player_id " \
            "> rw2.player_id);"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def newTournament():
    """Starts new tournament by removing all records in players and matches."""
    deleteMatches()
    deletePlayers()
