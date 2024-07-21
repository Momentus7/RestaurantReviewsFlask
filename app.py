# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mpag@88rbtsm'
app.config['MYSQL_DB'] = 'reviews_db'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM accounts WHERE username = % s \
			AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg=msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'cuisine' in request.form and 'ambience' in request.form and 'cleanliness' in request.form and 'food' in request.form and 'remarks' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cuisine = request.form['cuisine']
		ambience = request.form['ambience']
		cleanliness = request.form['cleanliness']
		food = request.form['food']
		remarks = request.form['remarks']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO accounts VALUES \
			(NULL, % s, % s, % s, % s, % s, % s, % s, % s)',
						(username, password, email, 
							cuisine, ambience, cleanliness,
							food, remarks))
			mysql.connection.commit()
			msg = 'You have successfully given your review !'
	elif request.method == 'POST':
		msg = 'Please fill out the review form !'
	return render_template('register.html', msg=msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account=account)
	return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'cuisine' in request.form and 'ambience' in request.form and 'cleanliness' in request.form and 'food' in request.form and 'remarks' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			cuisine = request.form['cuisine']
			ambience = request.form['ambience']
			cleanliness = request.form['cleanliness']
			food = request.form['food']
			remarks = request.form['remarks']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(
				'SELECT * FROM accounts WHERE username = % s',
					(username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s,\
				password =% s, email =% s, cuisine =% s, \
				ambience =% s, cleanliness =% s, food =% s, \
				remarks =% s WHERE id =% s', (
					username, password, email, cuisine, ambience, cleanliness,
							food, remarks, 
				(session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated your review!'
		elif request.method == 'POST':
			msg = 'Please fill out the review update form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(host="localhost", port=int("5000"))

