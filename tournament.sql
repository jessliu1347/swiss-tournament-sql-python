-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament
CREATE TABLE players (player_id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE matches(match_id SERIAL PRIMARY KEY, 
		winner INTEGER REFERENCES players(player_id),
		loser INTEGER REFERENCES players(player_id));
CREATE VIEW winners AS SELECT players.player_id, count(matches.winner) as wins
			FROM players LEFT JOIN matches ON players.player_id = matches.winner
			GROUP BY players.player_id
			ORDER BY wins DESC;
CREATE VIEW num_matches AS SELECT players.player_id, count(matches.match_id) as num_match
			FROM players LEFT JOIN matches ON (players.player_id = matches.winner
			OR players.player_id = matches.loser)
			GROUP BY players.player_id;
CREATE VIEW ranked_wins AS SELECT *, CEILING((1.0/2)*ROW_NUMBER() OVER (ORDER BY wins DESC)) AS rank
			FROM winners;
CREATE VIEW rw_withnames AS SELECT ranked_wins.player_id, players.name, ranked_wins.wins, ranked_wins.rank
			FROM ranked_wins JOIN players ON ranked_wins.player_id = players.player_id
			ORDER BY rank;
\q