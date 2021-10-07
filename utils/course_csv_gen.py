import csv, random

while True:
    write_csv = input("[W]rite to CSV or [P]rint to console?: ")

    if write_csv == 'W' or write_csv == 'w' or write_csv == 'P' or write_csv == 'p':
        break
    else:
        print('Invalid input. Please enter W or P [case insensitive].\n')
    

continue_input = 'Y'

# Print Course IDs to the terminal
if write_csv == 'P' or write_csv == 'p':
    while continue_input == 'Y' or continue_input == 'y':
        course_code = input("\nCourse code [ex. COP3014]: ")
        instructor = input("Instructor CS email [excluding @cs.fsu.edu]: ")

        to_hash = course_code + instructor

        id = hash(to_hash)
        if id < 0:
            id *= -1

        print('\n' + 'Course ID: ' + str(id)[:8] + '\n')

        continue_input =     input("Enter another [y/n]: ")

# Write Course Data to CSV file for Django import
else:
    try:
        with open("courses.csv", "w") as f:
            coursewriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            coursewriter.writerow(['id', 'code', 'name', 'instructor'])
            used_ids = []
            
            while continue_input == 'Y' or continue_input == 'y':
                course_code = input("\nCourse code [ex. COP3014]: ")
                course_name = input("Course name [ex. Programming I]: ")
                instructor = input("Instructor CS email [excluding @cs.fsu.edu]: ")

                correct_entry = input(
                    '\n'+course_code+'\t'+course_name+'\t'+instructor+"\n\nIs the entry correct [y/n]?: ")

                if correct_entry == 'N' or correct_entry =='n':
                    continue

                to_hash = course_code + instructor

                id = hash(to_hash)
                if id < 0:
                    id *= -1

                id = str(id)[:8]

                while id in used_ids:
                    id_list = list(id)
                    random.shuffle(id_list)
                    id = ''.join(id_list)

                used_ids.append(id)


                coursewriter.writerow([id, course_code, course_name, instructor+'@cs.fsu.edu'])

                continue_input = input("Enter another [y/n]: ")
    except IOError:
        print('Error creating output file. Please retry.\n')
