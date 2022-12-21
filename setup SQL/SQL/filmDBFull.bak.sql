BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "film" (
	"film_id"	INTEGER,
	"film_name"	TEXT NOT NULL,
	"manufacturer_id"	INT NOT NULL,
	"film_iso"	INT NOT NULL,
	"process_id"	INT NOT NULL,
	"film_url"	TEXT,
	FOREIGN KEY("process_id") REFERENCES "process",
	FOREIGN KEY("manufacturer_id") REFERENCES "manufacturer",
	PRIMARY KEY("film_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "process" (
	"process_id"	INTEGER,
	"process_name"	TEXT NOT NULL,
	"process_wiki_url"	TEXT,
	PRIMARY KEY("process_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "manufacturer" (
	"manufacturer_id"	INTEGER,
	"manufacturer_name"	TEXT NOT NULL,
	"manufacturer_url"	TEXT,
	PRIMARY KEY("manufacturer_id" AUTOINCREMENT)
);
INSERT INTO "film" ("film_id","film_name","manufacturer_id","film_iso","process_id","film_url") VALUES (1,'Apollo',8,400,1,'https://dubblefilm.com/en-us/products/apollo-400-35mm-film'),
 (2,'50D',7,50,1,'https://cinestillfilm.com/products/50daylight-36exp-135-fine-grain-color-film-35mm-roll'),
 (3,'T200',6,200,1,'https://buymorefilm.com/products/reto-amber-t200-tungsten-35mm-27'),
 (4,'Fujicolor',3,200,1,'https://www.fujifilm.com/us/en/consumer/film-quicksnap/film/fujifilm-200'),
 (5,'Superia X-TRA',3,400,1,'https://www.fujifilm.com/us/en/consumer/film-quicksnap/film/superia-400'),
 (6,'ColorPlus',1,200,1,'https://www.kodak.com/global/plugins/acrobat/en/consumer/products/techInfo/e7022/E7022.pdf'),
 (7,'Ektar',1,100,1,''),
 (8,'Gold',1,100,1,''),
 (9,'Portra',1,160,1,'');
INSERT INTO "process" ("process_id","process_name","process_wiki_url") VALUES (1,'C-41','https://en.wikipedia.org/wiki/C-41_process'),
 (2,'E6','https://en.wikipedia.org/wiki/E-6_process'),
 (3,'BW Negative','https://en.wikipedia.org/wiki/Photographic_processing#Black_and_white_negative_processing'),
 (4,'BW Reversal','https://en.wikipedia.org/wiki/Photographic_processing#Black_and_white_reversal_processing'),
 (5,'Kodachrome','https://en.wikipedia.org/wiki/Kodachrome');
INSERT INTO "manufacturer" ("manufacturer_id","manufacturer_name","manufacturer_url") VALUES (1,'Kodak','https://www.kodak.com/en/motion/products/camera-films'),
 (2,'Ilford','https://www.ilfordphoto.com/black-white-film'),
 (3,'Fujifilm','https://www.fujifilm.com/us/en/business/professional-photography/film'),
 (4,'ADOX','https://www.adox.de/Photo/adox-the-brand/'),
 (5,'Foma','https://www.foma.cz/en/photomaterials'),
 (6,'Amber','https://retoproject.com/products/reto-amber-film'),
 (7,'CineStill','https://cinestillfilm.com'),
 (8,'Doublefilm','https://dubblefilm.com/en-us'),
 (9,'AgfaPhoto','https://www.lupus-imaging-media.com/en/agfaphoto-apx/'),
 (10,'Arista EDU','https://en.wikipedia.org/wiki/List_of_photographic_films#Arista_EDU');
COMMIT;
