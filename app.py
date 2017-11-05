from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_login import login_required, logout_user, login_user, LoginManager
import os
from login import check_password
app = Flask(__name__)
 
@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')
 
@app.route('/login', methods=['POST'])
def login():
	username = str(request.form['username'])
	password = str(request.form['password'])
	if check_password(username, password):
		session['logged_in'] = True
	else:
		flash("wrong pass")
	return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

 
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	lm = LoginManager()
	lm.init_app(app)
	lm.login_view = 'login'
	app.run(debug=True)
