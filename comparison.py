import database

def find_all_friends_free_time(user_email):
	pass

def find_shared_free_time(user_email, friend_email, day):
	user_classes = database.get_user_classes(user_email.upper(), day)
	friend_classes = database.get_user_classes(friend_email.upper(), day)
	user_free_time = find_free_time(user_classes)
	friend_free_time = find_free_time(friend_classes)
	shared_free_time = []
	for x in user_free_time:
		for y in friend_free_time:
			if y[0] <= x[0] < y[1] or y[0] < x[1] <= y[1]:
				shared_free_time.append([max(x[0], y[0]), min(x[1], y[1])])
	return shared_free_time


def find_free_time(schedule):
	free_time = []
	start = "00"
	for interval in schedule:
		if start < interval[1]:
			free_time.append([start, interval[1]])
			start = interval[2]
	if schedule[-1][1] < "24:00":
		free_time.append([schedule[-1][2], "24:00"])
	return free_time

if __name__ == "__main__":
	print(find_shared_free_time("user1", "user2"))