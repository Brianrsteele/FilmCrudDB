/*
To initialize sqlite3 database:

	sqlite3 filmDB.db < filmDB.sql

References:	
	https://www.tutorialspoint.com/sqlite/sqlite_create_table.htm
*/

/*
TODO
- Create a color balance table and color balance foreign key in film
- Create a film_format table
- create a table to join film to film formats
- create a vendors table and join table to connect film with vendors

*/

/* Insert some common films into film table */
INSERT INTO film (film_name, manufacturer_id, film_iso, process_id,
					film_url) 
VALUES 
	("Apollo", 8, 400, 1, "https://dubblefilm.com/en-us/products/apollo-400-35mm-film"),
	("50D", 7, 50, 1, "https://cinestillfilm.com/products/50daylight-36exp-135-fine-grain-color-film-35mm-roll"),
	("T200", 6, 200, 1, "https://buymorefilm.com/products/reto-amber-t200-tungsten-35mm-27"),
	("Fujicolor", 3, 200, 1, "https://www.fujifilm.com/us/en/consumer/film-quicksnap/film/fujifilm-200"),
	("Superia X-TRA", 3, 400, 1, "https://www.fujifilm.com/us/en/consumer/film-quicksnap/film/superia-400"),
	("ColorPlus", 1, 200, 1, "https://www.kodak.com/global/plugins/acrobat/en/consumer/products/techInfo/e7022/E7022.pdf"),
	("Ektar", 1, 100, 1, ""),
	("Gold", 1, 100, 1, ""),
	("Portra", 1, 160, 1, "");

/* Insert some common values into processes table */
INSERT INTO process (process_name, process_wiki_url) 
VALUES 
	("C-41", "https://en.wikipedia.org/wiki/C-41_process"),
	("E6", "https://en.wikipedia.org/wiki/E-6_process"),
	("BW Negative", "https://en.wikipedia.org/wiki/Photographic_processing#Black_and_white_negative_processing"),
	("BW Reversal", "https://en.wikipedia.org/wiki/Photographic_processing#Black_and_white_reversal_processing");

/* Insert film manufacturers info to get started */
INSERT INTO manufacturer(manufaturer_name, manufacturer_url) 
VALUES 
	("Kodak", "https://www.kodak.com/en/motion/products/camera-films"),
	("Ilford", "https://www.ilfordphoto.com/black-white-film"),
	("Fujifilm","https://www.fujifilm.com/us/en/business/professional-photography/film"),
	("ADOX", "https://www.adox.de/Photo/adox-the-brand/"),
	("Foma", "https://www.foma.cz/en/photomaterials"),
	("Amber", "https://retoproject.com/products/reto-amber-film"),
	("CineStill", "https://cinestillfilm.com"),
	("Doublefilm", "https://dubblefilm.com/en-us");
