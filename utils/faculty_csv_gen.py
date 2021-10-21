import csv

try:
	with open("faculty.csv", "w") as f:
		facultywriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		facultywriter.writerow(['email', 'first_name', 'last_name'])

		continue_input = 'Y'

		while continue_input == 'Y' or continue_input == 'y':
			instructor_id = input("\nInstructor CS email [excluding @cs.fsu.edu]: ")
			first_name = input("Faculty first name: ")
			last_name = input("Faculty last name: ")
			
			correct_entry = input(
				'\n'+instructor_id+'\t'+first_name+'\t'+last_name+"\n\nIs the entry correct [y/n]?: ")

			if correct_entry == 'N' or correct_entry == 'n':
				continue

			facultywriter.writerow(
				[instructor_id+'@cs.fsu.edu', first_name, last_name])

			continue_input = input("Enter another [y/n]: ")
except IOError:
	print('Error creating output file. Please retry.\n')
