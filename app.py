from flask import Flask, g
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_login import login_required, logout_user, login_user, LoginManager
import os
import database
from user_management import check_password
app = Flask(__name__)

 
@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html', user = g.user)
@app.route('/refresh_index')
def refresh_index():
	return render_template('index.html', user="no")

@app.route('/add_classes')
def add_classes():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('add_classes.html')

@app.route('/submit_classes', methods=['POST'])
def submit_classes():
	class1 = str(request.form['class1'])
	class2 = str(request.form['class2'])
	print(class1 + class2)

 
@app.route('/login', methods=['POST'])
def login():
	username = str(request.form['username'])
	password = str(request.form['password'])
	if check_password(username, password):
		session['logged_in'] = True
		g.user = username
	else:
		flash("Incorrect Username or Password")
	return index()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	g.user = None
	return index()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)
