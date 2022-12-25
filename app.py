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
    film_info = film_list_query()
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
        film_insert_query(film_details)
        return render_template('add_film_success.html', title='Successfully Added Film')

# ------------------------ Manufacturer Pages ------------------------

@app.route('/manufacturers', methods = ['GET','POST'])
def manufacturers():
    # render a list of all of the manufacturers in the database if 
    # the request is a GET request.
    # if the request is a POST request,
    # print the success message with the manufacturer
    # added
    if request.method == 'GET':
        manufacturer_id = request.args.get('manufacturer_id')
        manufacturer_info = manufacturer_list_query()
        return render_template('manufacturer/manufacturers.html', manufacturer_info=manufacturer_info, title='Manufacturers')
    if request.method == 'POST':
        # this is an edit from edit_process.html
        if 'manufacturer_id' in request.form:
            manufacturer_details = (
                request.form['manufacturer_id'],
                request.form['manufacturer_name'],
                request.form['manufacturer_url']
            )
            manufacturer_update_query(manufacturer_details)
            manufacturer_info = manufacturer_list_query()
            title = 'Successfully edited ' + manufacturer_details[1]
            edit_success = True
            manufacturer_name=manufacturer_details[1]
            return render_template('manufacturer/manufacturers.html', manufacturer_info=manufacturer_info, title=title, edit_success=edit_success, manufacturer_name=manufacturer_name)
        # this is an add from add_process.html
        if 'manufacturer_id' not in request.form:
            manufacturer_details = (
                request.form['manufacturer_name'],
                request.form['manufacturer_url']
            )
            manufacturer_insert_query(manufacturer_details)
            manufacturer_info = manufacturer_list_query()
            title = 'Successfully added ' + manufacturer_details[0]
            add_success = True
            manufacturer_name=manufacturer_details[0]
            return render_template('manufacturer/manufacturers.html', manufacturer_info=manufacturer_info, title=title, add_success=add_success, manufacturer_name=manufacturer_name)

@app.route('/add_manufacturer')
def add_manufacturer():
    # add a process to the database. 
    return render_template('manufacturer/add_manufacturer.html', title='Add Manufacturer')

@app.route('/<manufacturer_id>/delete_manufacturer', methods=['GET','POST'])
def delete_manufacturer(manufacturer_id):  
    # use manufacturer_details to get the name of the process
    manufacturer_details = manufacturer_detail_query(manufacturer_id)
    manufacturer_name = manufacturer_details[1]
    manufacturer_remove_query(manufacturer_id)  
    # use manufacturer info to populate the table
    manufacturer_info = manufacturer_list_query()
    title = 'Successfully deleted ' + manufacturer_id
    delete_success = True
    return render_template('manufacturer/manufacturers.html', manufacturer_info=manufacturer_info, title=title, delete_success=delete_success, 
                                        manufacturer_id=manufacturer_id, manufacturer_name=manufacturer_name)

@app.route('/<manufacturer_id>/edit_manufacturer')  
def edit_manufacturer(manufacturer_id):
    # update a process to the database
    manufacturer_details = manufacturer_detail_query(manufacturer_id)
    return render_template('manufacturer/edit_manufacturer.html', manufacturer_details=manufacturer_details)

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
        process_info = process_list_query()
        return render_template('process/process.html', process_info=process_info, title='Processes')
    if request.method == 'POST':
        # this is an edit from edit_process.html
        if 'process_id' in request.form:
            print('process id, editing.')
            process_details = (
                request.form['process_id'],
                request.form['process_name'],
                request.form['process_wiki_url']
            )
            process_update_query(process_details)
            process_info = process_list_query()
            title = 'Successfully edited ' + process_details[1]
            edit_success = True
            process_name=process_details[1]
            return render_template('process/process.html', process_info=process_info, title=title, edit_success=edit_success, process_name=process_name)
        # this is an add from add_process.html
        if 'process_id' not in request.form:
            print('no process id, adding')
            process_details = (
                request.form['process_name'],
                request.form['process_wiki_url']
            )
            process_insert_query(process_details)
            process_info = process_list_query()
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
    process_details = process_detail_query(process_id)
    process_name = process_details[1]
    process_remove_query(process_id)  
    # use process info to populate the table
    process_info = process_list_query()
    title = 'Successfully deleted ' + process_id
    delete_success = True
    return render_template('process/process.html', process_info=process_info, title=title, delete_success=delete_success, 
                                            process_id=process_id, process_name=process_name)

@app.route('/<process_id>/edit_process')  
def edit_process(process_id):
    # update a process to the database
    process_details = process_detail_query(process_id)
    return render_template('process/edit_process.html', process_details=process_details)

# ------------------------------------------------------------------------------
#                          Querries
# ------------------------------------------------------------------------------

# ----------------------- Film Querries ------------------------

def film_list_query():
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT  film.film_id, manufacturer.manufacturer_name, film.film_name, film.film_iso, process.process_name, film.film_url
    FROM film INNER JOIN manufacturer ON film.manufacturer_id = manufacturer.manufacturer_id
    INNER JOIN process ON film.process_id = process.process_id
    ORDER BY film.film_name;
    """)
    film_info = cursor.fetchall()
    connection.commit()
    connection.close()
    return film_info

def film_insert_query(film_details):
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

def manufacturer_list_query():
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT manufacturer_id, manufacturer_name, manufacturer_url FROM manufacturer
    ORDER BY manufacturer_name;
    """)
    manufacturer_info = cursor.fetchall()
    connection.commit()
    connection.close()
    return manufacturer_info

def manufacturer_detail_query(manufacturer_id):
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    sql_execute_string = """
    SELECT * FROM manufacturer
    WHERE manufacturer_id = (?)
    """
    cursor.execute(sql_execute_string, (manufacturer_id,))
    process_details = cursor.fetchone()
    connection.commit()
    connection.close()
    return process_details

def manufacturer_insert_query(manufacturer_details):
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

def manufacturer_remove_query(manufacturer_id):
    # Insert details for a new process into db.
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_execute_string = """
    DELETE FROM manufacturer WHERE manufacturer_id = (?)
    """
    # second parameter of cursor.execute must be a tuple
    # force it with an extra , if you have to.
    cursor.execute(sql_execute_string, (manufacturer_id,))
    connection.commit()
    connection.close()

def manufacturer_update_query(manufacturer_details):
    # Insert details for a new process into db.
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_execute_string = """
    UPDATE manufacturer 
    SET manufacturer_name = (?), manufacturer_url = (?) WHERE manufacturer_id = (?);
    """
    # second parameter of cursor.execute must be a tuple
    # force it with an extra , if you have to.
    cursor.execute(sql_execute_string, (manufacturer_details[1], manufacturer_details[2], manufacturer_details[0] ))
    connection.commit()
    connection.close()

# ----------------------- Process Querries ------------------------

def process_list_query():
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

def process_detail_query(process_id):
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

def process_insert_query(process_details):
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

def process_remove_query(process_id):
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

def process_update_query(process_details):
    # Insert details for a new process into db.
    db_file = 'filmDB.db'
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_execute_string = """
    UPDATE process 
    SET process_name = (?), process_wiki_url = (?) WHERE process_id = (?);
    """
    # second parameter of cursor.execute must be a tuple
    # force it with an extra , if you have to.
    cursor.execute(sql_execute_string, (process_details[1], process_details[2], process_details[0] ))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    app.run()