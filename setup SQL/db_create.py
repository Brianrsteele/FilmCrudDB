import sqlite3


# https://youtu.be/cGWP9FRMQLw

db_file = 'filmDB.db'

connection = sqlite3.connect(db_file)
cursor = connection.cursor()

cursor.execute("""

CREATE TABLE film (
	film_id	INTEGER PRIMARY KEY AUTOINCREMENT,
	film_name	TEXT	NOT NULL,
	manufacturer_id	INT	NOT NULL REFERENCES manufacturer,
	film_iso	INT NOT NULL,
	process_id INT NOT NULL	REFERENCES process,	
	film_url TEXT
);

""")

cursor.execute("""
CREATE TABLE process (
	process_id	INTEGER	PRIMARY KEY	AUTOINCREMENT,
	process_name	TEXT	NOT NULL,
	process_wiki_url	TEXT
);
""")

cursor.execute("""
CREATE TABLE manufacturer (
	manufacturer_id	INTEGER		PRIMARY KEY		AUTOINCREMENT,
	manufacturer_name	TEXT	NOT NULL,
	manufacturer_url	TEXT
);
""")



connection.commit()
connection.close()