#
# Lots of the code in here is directly from 
# http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup
# See README for more info
#

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3

DATABASE = 'todo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

conn = None

app = Flask(__name__)

def get_conn():
    #tells interpreter to use conn defined above
    global conn
    if conn is None:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_connection(exception):
    global conn
    if conn is not None:
        conn.close()
        conn = None
        
def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query, args)
    
	#result
    r = cur.fetchall()
    cur.close()
    return (r[0] if r else None) if one else r
    
def add_task(category, priority, description):
    tasks = query_db('insert into tasks values(?,?,?)', [category, priority, description], one = False)
   
    #needed for saving in database
    get_conn().commit()

@app.route('/login')
def login():
	error = "test"
	return render_template('login.html', errors=error)

@app.route('/')
@app.route('/show_entries')
def show_entries():
	db_result = query_db("select * from tasks")
	entries = [dict(category=row[0], priority=row[1], description=row[2]) for row in db_result]
	return render_template('show_entries.html', entries=entries)	


if __name__ == '__main__':
    app.debug = True
    app.run()

    