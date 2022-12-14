/*
To initialize sqlite3 database:

	sqlite3 filmDB.db < filmDB.sql

References:	
	https://www.tutorialspoint.com/sqlite/sqlite_create_table.htm
*/

/* Create a film table */
CREATE TABLE film (
	film_id	INTEGER PRIMARY KEY AUTOINCREMENT,
	film_name	TEXT	NOT NULL,
	manufacturer_id	INT	NOT NULL REFERENCES manufacturer,
	film_iso	INT NOT NULL,
	process_id INT NOT NULL	REFERENCES process,	
	film_url TEXT
);

/* Create a processes table */
CREATE TABLE process (
	process_id	INTEGER	PRIMARY KEY	AUTOINCREMENT,
	process_name	TEXT	NOT NULL,
	process_wiki_url	TEXT
);

/* Create a film manufacturers table*/
CREATE TABLE manufacturer (
	manfacturer_id	INTEGER		PRIMARY KEY		AUTOINCREMENT,
	manufaturer_name	TEXT	NOT NULL,
	manufacturer_url	TEXT
);

/* Insert film manufacturers info to get started */

