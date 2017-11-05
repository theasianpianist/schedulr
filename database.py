import re
import sqlite3 as sql
import sys
import itertools

db_name = "test.db"
con = None

def put_classes(user, classes, starts, ends, days):
	user = user.upper()
	schedule = [[course, start, end] for course, start, end in itertools.zip_longest(classes, starts, ends)]
	week = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			for index in range(len(days)):
				for i, x in itertools.zip_longest(week, days[index]):
					if x is not None:
						cur.execute("SELECT (%s) FROM main WHERE email = ?" % i, (user,))
						old = cur.fetchone()[0]
						if old is not None:
							arg = old + "," + str(schedule[index])
						else:
							arg = schedule[index]
						cur.execute("UPDATE main SET (%s) = ? WHERE email = ?" % i, (str(arg), user))
	except sql.Error as error:
		print("Error: %s" % str(error))
	finally:
		if con:
			con.close()

def put_friends(user, friends):
	user = user.upper()
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute('''UPDATE main SET friends = ? WHERE email = ?''', (friends, user))
	except sql.Error as error:
		print("Error %s", str(error))
	finally:
		if con:
			con.close()

def get_user_classes(user_email, day):
	classes = []
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute("SELECT (%s) FROM main WHERE email = ?" % str(day), (user_email,))
			classes = cur.fetchall()
			if classes and classes[0][0]:
				classes = eval("[" + classes[0][0] + "]")
			else:
				return [(None,)]
	except sql.Error as error:
		print("Error %s", str(error))
		sys.exit(1)
	finally:
		if con:
			con.close()
	return classes

def get_friends(user_email):
	user_email = user_email.upper()
	friends = []
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute('''SELECT friends FROM main WHERE email = ?''', (user_email,))
			friends = cur.fetchall()
			friends = eval(friends[0][0])
	except sql.Error as error:
		print("Error %s", str(error))
		sys.exit(1)
	finally:
		if con:
			con.close()
	return friends

if __name__ == "__main__":
	days = [[None, 'on', None, 'on', None, 'on', None], [None, None, None, None, None, None, None], [None, None, None, None, None, None, None], [None, None, None, None, None, None, None], [None, None, None, None, None, None, None], [None, None, None, None, None, None, None], [None, None, None, None, None, None, None]]
	classes = ['CMPSC 311', '', '', '', '', '', '']
	starts = ['15:35', '', '', '', '', '', '']
	ends = ['16:25', '', '', '', '', '', '']
	put_classes("user1@psu.edu", classes, starts, ends, days)

