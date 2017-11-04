import re
import sqlite3 as sql
import sys

db_name = "test.db"
con = None
#
# def get_input():
# 	num_classes = input("How many classes do you have? ")
# 	num_pattern = re.compile("^[0-9]+$")
# 	while not num_pattern.match(num_classes):
# 		print("Please enter a valid number")
# 		num_classes = input("How many classes do you have? ")
# 	num_classes = int(num_classes)
# 	schedule = []
# 	for i in range(num_classes):
# 		course = []
# 		course.append(input("Name of class " + str(i + 1) + ": ").upper())
# 		course.append(input("Start time of class " + str(i + 1) + ": ").upper())
# 		course.append(input("End time of class " + str(i + 1) + ": ").upper())
# 		schedule.append(course)
# 	return schedule

def put_db(user, schedule, friends = None):
	user_sanitized = user.upper()
	schedule_sanitized = schedule
	friends_sanitized = []
	if friends:
		friends_sanitized = [x.upper() for x in friends]
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute('''CREATE TABLE IF NOT EXISTS main(email TEXT PRIMARY KEY, classes TEXT, friends TEXT)''')
			cur.execute('''INSERT INTO main VALUES(?, ?, ?)''', (str(user_sanitized), str(schedule_sanitized), str(friends_sanitized)))
	except sql.Error as error:
		print("Error %s", str(error))
		sys.exit(1)
	finally:
		if con:
			con.close()

def get_user_classes(user_email):
	classes = []
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute('''SELECT classes FROM main WHERE email = ?''', (user_email,))
			classes = cur.fetchall()
			classes = eval(classes[0][0])
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
	# friendsa = ["user2"]
	# friendsb = ["user1"]
	# schd = get_input()
	# put_db("user1", schd, friendsa)
	# schd = get_input()
	# put_db("user2", schd, friendsb)
	friends = get_friends("user1")
	friend_classes = []
	for x in friends:
		friend_classes.append([x, get_user_classes(x)])
	print(friend_classes)

