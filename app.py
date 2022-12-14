from flask import Flask, render_template, request
import sqlite3

# https://youtu.be/cGWP9FRMQLw
# https://youtu.be/hfPLX9fufpo

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html', title='Home')
    

@app.route('/film')
def film():
    film_info = query_film_info()
    return render_template('film.html', film_info=film_info, title='Film')

@app.route('/manufacturers')
def manufacturers():
    manufacturers_info = query_manufacturer_info()
    return render_template('manufacturers.html', manufacturers_info=manufacturers_info, title='Manufacturers')


@app.route('/processes')
def processes():
    process_info = query_process_info()
    return render_template('process.html', process_info=process_info, title='Processes')

@app.route('/add_film', methods = ['GET','POST'])
def add_film():
    if request.method == 'GET':
        return render_template('add_film.html')
    else:
        film_details = (
            request.form['film_name'],
            request.form['manufacturer_id'],
            request.form['film_iso'],
            request.form['process_id'],
            request.form['film_url']
        )
        insert_film(film_details)
        return render_template('add_success.html', title='Add Film')

def insert_film(film_details):
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_execute_string = """
    INSERT INTO film (film_name, manufacturer_id, film_iso, process_id, film_url)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(sql_execute_string, film_details)
    connection.commit()
    connection.close()



def query_film_info():
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT  manufacturer.manufacturer_name,film.film_name,  film.film_iso, process.process_name, film.film_url
    FROM film INNER JOIN manufacturer ON film.manufacturer_id = manufacturer.manufacturer_id
    INNER JOIN process ON film.process_id = process.process_id
    ORDER BY film.film_name;
    """)
    film_info = cursor.fetchall()
    connection.commit()
    connection.close()
    return film_info

def query_manufacturer_info():
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT manufacturer_name, manufacturer_url FROM manufacturer
    ORDER BY manufacturer_name;
    """)
    manufacturer_info = cursor.fetchall()
    connection.commit()
    connection.close()
    return manufacturer_info

def query_process_info():
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT process_name, process_wiki_url FROM process
    ORDER BY process_name;
    """)
    manufacturer_info = cursor.fetchall()
    connection.commit()
    connection.close()
    return manufacturer_info

if __name__ == '__main__':
    app.run()