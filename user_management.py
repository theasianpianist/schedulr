import sqlite3 as sql
import bcrypt
import unicodedata

db_name = "test.db"
def check_password(user_email, password):
	user_email = user_email.upper()
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute('''SELECT pass FROM main WHERE email = ?''', (user_email,))
			tpass = cur.fetchall()
			if tpass:
				hashed = tpass[0][0]
				if bcrypt.checkpw(password.encode('utf-8'), hashed):
					return True
			return False
	except sql.Error as error:
		print("Error %s", str(error))
	finally:
		if con:
			con.close()

def add_user(email, password):
	email = email.upper()
	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO main (email, pass) VALUES (?, ?)", (email, hashed))
	except sql.Error as error:
		print("Error %s", str(error))
		return False
	finally:
		if con:
			con.close()
		return True



def add_friend(user_email, friend_email):
	user_email = user_email.upper()
	friend_email = friend_email.upper()
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute("SELECT friends FROM main WHERE email = ?", (user_email,))
			old_friends = cur.fetchone()[0]
			if old_friends:
				new_friends = eval(old_friends)
				new_friends.add(friend_email)
			else:
				new_friends = [friend_email]
			cur.execute("UPDATE main SET friends = ? WHERE email = ?", (str(new_friends), user_email))
	except sql.Error as error:
		print("Error %s" % str(error))
	finally:
		if con:
			con.close()

if __name__ == "__main__":
	add_friend("user1@psu.edu", "user3@psu.edu")