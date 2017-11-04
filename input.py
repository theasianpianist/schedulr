import re

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
		course.append(input("Name of class " + str(i + 1) + ": "))
		course.append(input("Start time of class " + str(i + 1) + ": "))
		course.append(input("End time of class " + str(i + 1) + ": "))
		schedule.append(course)
	return schedule

if __name__ == "__main__":
	print(get_input())
