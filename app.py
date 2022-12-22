from flask import Flask, render_template, request
import sqlite3

# https://youtu.be/cGWP9FRMQLw
# https://youtu.be/hfPLX9fufpo
# https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for

app = Flask(__name__)

# ------------------------------------------------------------------------------
#                          Routes
# ------------------------------------------------------------------------------

@app.route('/')
@app.route('/home')
def home_page():
    # render a home page
    return render_template('index.html', title='Home')
    
# ------------------------ Film Pages ------------------------
@app.route('/film')
def film():
    # render a list of all of the films in database.
    film_info = query_film_info()
    return render_template('film.html', film_info=film_info, title='Film')

@app.route('/add_film', methods = ['GET','POST'])
def add_film():
    # add a film to the database. If the request is a GET request,
    # then render a form to collect film inforamation
    # if it is a POST request, then send film details to
    # insert method
    if request.method == 'GET':
        return render_template('add_film.html', title='Add Film')
    else:
        film_details = (
            request.form['film_name'],
            request.form['manufacturer_id'],
            request.form['film_iso'],
            request.form['process_id'],
            request.form['film_url']
        )
        insert_film(film_details)
        return render_template('add_film_success.html', title='Successfully Added Film')

# ------------------------ Manufacturer Pages ------------------------

@app.route('/manufacturers')
def manufacturers():
    # Render a list of all of the manufacturers
    manufacturers_info = query_manufacturer_info()
    return render_template('manufacturers.html', manufacturers_info=manufacturers_info, title='Manufacturers')

@app.route('/add_manufacturer', methods = ['GET', 'POST'])
def add_manufacturer():
    # addmanufacturer to the database. If the request is a GET request,
    # then render a form to collect manufacturer inforamation
    # if it is a POST request, then send manufacturer details to
    # insert method
    if request.method == 'GET':
        return render_template('add_manufacturer.html', title='Add Manufacturer')
    else:
        manufacturer_details = (
            request.form['manufacturer_name'],
            request.form['manufacturer_url'],
        )
        insert_manufacturer(manufacturer_details)
        return render_template('add_manufacturer_success.html', title='Successfully Added Manufacturer')

# ----------------------- Process Pages ------------------------

@app.route('/processes', methods = ['GET','POST'])
def processes():
    # render a list of all of the processes in the database if 
    # the request is a GET request.
    # if the request is a POST request,
    # print the success message with the process
    # added
    if request.method == 'GET':
        process_id = request.args.get('process_id')
        process_info = query_process_info()
        return render_template('process/process.html', process_info=process_info, title='Processes')
    if request.method == 'POST':
        process_details = (
            request.form['process_name'],
            request.form['process_wiki_url']
        )
        insert_process(process_details)
        process_info = query_process_info()
        title = 'Successfully added ' + process_details[0]
        add_success = True
        process_name=process_details[0]
        return render_template('process/process.html', process_info=process_info, title=title, add_success=add_success, process_name=process_name)

@app.route('/add_process')
def add_process():
    # add a process to the database. 
    return render_template('process/add_process.html', title='Add Process')

@app.route('/<process_id>/delete_process', methods=['GET','POST'])
def delete_process(process_id):  
    
    # use process_details to get the name of the process
    process_details = query_process_detail(process_id)
    process_name = process_details[1]
    remove_process(process_id)  
    # use process info to populate the table
    process_info = query_process_info()
    title = 'Successfully deleted ' + process_id
    delete_success = True
    return render_template('process/process.html', process_info=process_info, title=title, delete_success=delete_success, 
                                            proces_id=process_id, process_name=process_name)
    

# ------------------------------------------------------------------------------
#                          Querries
# ------------------------------------------------------------------------------

# ----------------------- Film Querries ------------------------

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

# ----------------------- Manufacturer Querries ------------------------

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

def insert_manufacturer(manufacturer_details):
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_execute_string = """
    INSERT INTO manufacturer (manufacturer_name, manufacturer_url)
    VALUES (?, ?)
    """
    cursor.execute(sql_execute_string, manufacturer_details)
    connection.commit()
    connection.close()

# ----------------------- Process Querries ------------------------

def query_process_info():
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT process_id, process_name, process_wiki_url FROM process
    ORDER BY process_name;
    """)
    manufacturer_info = cursor.fetchall()
    connection.commit()
    connection.close()
    return manufacturer_info

def query_process_detail(process_id):
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    sql_execute_string = """
    SELECT * FROM process
    WHERE process_id = (?)
    """
    cursor.execute(sql_execute_string, (process_id,))
    process_details = cursor.fetchone()
    connection.commit()
    connection.close()
    return process_details

def insert_process(process_details):
    # Insert details for a new process into db.
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_execute_string = """
    INSERT INTO process (process_name, process_wiki_url)
    VALUES (?, ?)
    """
    cursor.execute(sql_execute_string, process_details)
    connection.commit()
    connection.close()

def remove_process(process_id):
    # Insert details for a new process into db.
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_execute_string = """
    DELETE FROM process WHERE process_id = (?)
    """
    # second parameter of cursor.execute must be a tuple
    # force it with an extra , if you have to.
    cursor.execute(sql_execute_string, (process_id,))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    app.run()