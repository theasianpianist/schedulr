import sqlite3 as sql
db_name = "test.db"
def check_password(user_email, password):
	user_email = user_email.upper()
	try:
		con = sql.connect(db_name)
		with con:
			cur = con.cursor()
			cur.execute('''SELECT pass FROM main WHERE email = ?''', (user_email,))
			tpass = cur.fetchall()
			if password == tpass[0][0]:
				return True
			return False
	except sql.Error as error:
		print("Error %s", str(error))
	finally:
		if con:
			con.close()