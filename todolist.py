#
# Lots of the code in here is directly from 
# http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup
# See README for more info
#

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3

DATABASE = 'todo.db'
DEBUG = True
SECRET_KEY = 'blah blah blah'
USERNAME = 'a'
PASSWORD = 'b'

app = Flask(__name__)
app.config.from_object(__name__)

conn = None

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
    	abort(401)
	g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/')
@app.route('/show_entries')
def show_entries():
	db_result = query_db("select * from tasks")
	entries = [dict(category=row[0], priority=row[1], description=row[2]) for row in db_result]
	return render_template('show_entries.html', entries=entries)	


if __name__ == '__main__':
    app.debug = True
    app.run()

    