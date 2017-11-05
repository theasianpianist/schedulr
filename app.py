from flask import Flask, g
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_login import login_required, logout_user, login_user, LoginManager, current_user, UserMixin, login_manager
import os
import database
from user_management import check_password
app = Flask(__name__)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

class User(UserMixin):
	def __init__(self, id):
		self.id = id
		self.name = "user" + str(id)
		self.password = self.name + "_secret"

	def __repr__(self):
		return "%s/%s/%s" % (self.id, self.name, self.password)

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html', user = g.user.get_id())

@app.route('/add_classes')
def add_classes():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('add_classes.html')

@app.route('/submit_classes', methods=['POST'])
def submit_classes():
	week = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
	classes = []
	starts = []
	ends = []
	days = []
	for i in range(7):
		classes.append(str(request.form['class' + str(i + 1)]))
		starts.append(request.form['start' + str(i + 1)])
		ends.append(request.form['end' + str(i + 1)])
		if starts[i] > ends[i]:
			flash("A class cannot start after it ends")
			return render_template('add_classes.html')
		class_days = []
		for day in week:
			form = day + str(i + 1)
			class_days.append(request.form.get(form))
		if class_days.count(None) == len(class_days) and classes[i] != "":
			flash("Please select at least one day per class")
			return render_template('add_classes.html')
		days.append(class_days)
	if classes.count("") == len(classes):
		flash("Please enter at least one class")
		return render_template('add_classes.html')
	if starts.count("") != classes.count(""):
		flash("Please enter a start time for every class")
		return render_template('add_classes.html')
	if starts.count("") != ends.count(""):
		flash("Please enter an end time for every class")
		return render_template('add_classes.html')
	database.put_classes(g.user.get_id(), classes, starts, ends, days)
	return index()
 
@app.route('/login', methods=['GET','POST'])
def login():
	username = str(request.form['username'])
	password = str(request.form['password'])
	if check_password(username, password):
		session['logged_in'] = True
		user = User(username)
		login_user(user)
	else:
		flash("Incorrect Username or Password")
	return index()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	logout_user()
	return index()

@lm.user_loader
def load_user(userid):
    return User(userid)

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)
