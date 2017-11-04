import re
import sqlite3 as sql
import sys

db_name = "test.db"
con = None

def get_input():
	num_classes = input("How many classes do you have? ")
	num_pattern = re.compile("^[0-9]+$")
	while not num_pattern.match(num_classes):
		print("Please enter a valid number")
		num_classes = input("How many classes do you have? ")
	num_classes = int(num_classes)
	schedule = []
	for i in range(num_classes):
		course = []
		course.append(input("Name of class " + str(i + 1) + ": ").upper())
		course.append(input("Start time of class " + str(i + 1) + ": ").upper())
		course.append(input("End time of class " + str(i + 1) + ": ").upper())
		schedule.append(course)
	return schedule

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




if __name__ == "__main__":
	schd = get_input()
	put_db("user1", schd)
