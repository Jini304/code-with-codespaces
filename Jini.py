import re  # Importing the regular expression (regex) module for pattern matching
from datetime import datetime  # Importing the datetime module to handle date and time

# Function to load data from text files
def load_data():
    try:
        # Load student data from 'students.txt'
        students = {}
        with open("students.txt", "r") as student_file:
            next(student_file)  # Skip the header row
            for line in student_file:
                student_id, name, contact = line.strip().split(',')  # Split each line by commas
                students[student_id] = {"Name": name, "Contact": contact}  # Store student data in a dictionary

        # Load course data from 'courses.txt'
        courses = {}
        with open("courses.txt", "r") as course_file:
            next(course_file)  # Skip the header row
            for line in course_file:
                course_id, name, seats = line.strip().split(',')  # Split each line by commas
                courses[course_id] = {"Name": name, "Seats": int(seats)}  # Store course data, converting seats to an integer

        # Load enrollment data from 'enrollments.txt'
        enrollments = {}
        with open("enrollments.txt", "r") as enrollment_file:
            next(enrollment_file)  # Skip the header row
            for line in enrollment_file:
                student_id, course_id, enrollment_date = line.strip().split(',')  # Split each line by commas
                enrollments.setdefault(student_id, []).append({"CourseID": course_id, "Date": enrollment_date})  # Store enrollment data

        return {"students": students, "courses": courses, "enrollments": enrollments}  # Return the data

    except FileNotFoundError:  # If files are not found, return empty dictionaries
        return {"students": {}, "courses": {}, "enrollments": {}}

# Function to save data back to text files
def save_data():
    # Save students data to 'students.txt'
    with open("students.txt", "w") as student_file:
        student_file.write("StudentID,Name,Contact\n")  # Write the header row
        for student_id, student_info in students.items():
            student_file.write(f"{student_id},{student_info['Name']},{student_info['Contact']}\n")  # Write each student's data

    # Save courses data to 'courses.txt'
    with open("courses.txt", "w") as course_file:
        course_file.write("CourseID,CourseName,AvailableSeats\n")  # Write the header row
        for course_id, course_info in courses.items():
            course_file.write(f"{course_id},{course_info['Name']},{course_info['Seats']}\n")  # Write each course's data

    # Save enrollments data to 'enrollments.txt'
    with open("enrollments.txt", "w") as enrollment_file:
        enrollment_file.write("StudentID,CourseID,EnrollmentDate\n")  # Write the header row
        for student_id, enrollments_list in enrollments.items():
            for enrollment in enrollments_list:
                enrollment_file.write(f"{student_id},{enrollment['CourseID']},{enrollment['Date']}\n")  # Write each enrollment's data

# Load existing data from files
storage = load_data()  # Load data from text files
students = storage["students"]
courses = storage["courses"]
enrollments = storage["enrollments"]

# Function to validate student ID
def is_valid_student_id(student_id):
    return student_id.isdigit() and len(student_id) == 8 and student_id not in students  # Check if student ID is valid and unique

# Function to validate student contact
def is_valid_contact(contact):
    return bool(re.fullmatch(r"01\d{8,9}", contact)) and not any(s['Contact'] == contact for s in students.values())  # Validate contact format and uniqueness

# Function to validate course ID
def is_valid_course_id(course_id):
    return bool(re.fullmatch(r"[A-Z]{3}\d{4}", course_id)) and course_id not in courses  # Check if course ID format is valid and unique

# Function to validate date
def is_valid_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")  # Try to parse the date
        return date <= datetime.today()  # Ensure the date is not in the future
    except ValueError:
        return False  # If invalid, return False

# Function to add a new student
def add_student():
    while True:
        student_id = input("Enter student ID (8-digit number): ").strip()
        if student_id in students or not student_id.isdigit() or len(student_id) != 8:
            print("Please enter a valid and unique student ID.")
            continue  # Prompt the user to enter again if invalid
        break  # If valid ID, break out of the loop

    name = input("Enter student name: ").strip().title()  # Capitalize the student's name

    while True:
        contact = input("Enter contact (10 or 11 digits starting with 01 without '-'): ").strip()  # Ask for contact number
        if re.fullmatch(r"01\d{8,9}", contact):
            break  # If valid contact, break out of the loop
        print("Please enter a valid and unique student contact.")  # If invalid, prompt again

    students[student_id] = {"Name": name, "Contact": contact}  # Store the new student data
    save_data()  # Save the updated data to the file
    print(f"Student {name} added successfully.")  # Inform the user that the student was added

# Function to add a new course
def add_course():
    while True:
        course_id = input("Enter course ID (3 uppercase letters + 4 digits, e.g., MPU7765): ").strip().upper()  # Ask for course ID
        if not is_valid_course_id(course_id):
            print("Please enter a valid and unique course ID.")
            continue  # If invalid, prompt again
        break  # If valid course ID, break out of the loop

    while True:
        course_name = input("Enter course name: ").strip().title()  # Ask for course name
        if re.fullmatch(r"^[A-Za-z ]+$", course_name) and not any(c['Name'] == course_name for c in courses.values()):
            break  # If valid course name and unique, break out of the loop
        print("Course name must be unique and in words. Please enter a valid course name.")  # Prompt again if invalid

    while True:
        seats = input("Enter available seats: ").strip()  # Ask for the number of available seats
        if seats.isdigit() and int(seats) > 0:
            seats = int(seats)
            break  # If valid number, break out of the loop
        print("Invalid seat count.")  # If invalid, prompt again

    courses[course_id] = {"Name": course_name, "Seats": seats}  # Store the new course data
    save_data()  # Save the updated data to the file
    print(f"Course {course_name} added successfully.")  # Inform the user that the course was added

# Function to enroll in a course
def enroll_in_course():
    student_id = input("Enter student ID: ").strip()  # Ask for student ID
    if student_id not in students:
        print("Student ID not found.")  # Check if student exists
        return

    course_id = input("Enter course ID: ").strip().upper()  # Ask for course ID
    if course_id not in courses:
        print("Course ID not found.")  # Check if course exists
        return
    if courses[course_id]['Seats'] <= 0:
        print("No seats available in this course.")  # Check if there are seats available
        return

    if student_id in enrollments and any(enrollment['CourseID'] == course_id for enrollment in enrollments[student_id]):
        print("Student is already enrolled in this course.")  # Check if student is already enrolled in the course
        return

    while True:
        enrol_date = input("Enter enrollment date (YYYY-MM-DD): ").strip()  # Ask for the enrollment date
        if is_valid_date(enrol_date):
            break  # If valid date, break out of the loop
        print("Please enter a valid enrollment date (not in the future).")  # Prompt again if date is invalid

    if student_id not in enrollments:
        enrollments[student_id] = []  # If the student has no enrollments, create an empty list
    enrollments[student_id].append({'CourseID': course_id, 'Date': enrol_date})  # Add the enrollment data
    courses[course_id]['Seats'] -= 1  # Reduce available seats in the course
    save_data()  # Save the updated data to the file
    print(f"{students[student_id]['Name']} ({student_id}) enrolled in {courses[course_id]['Name']} on {enrol_date}.")  # Inform the user

# Function to drop a course
def drop_course():
    student_id = input("Enter student ID: ").strip()  # Ask for student ID
    if student_id not in enrollments or not enrollments[student_id]:
        print("No enrolled courses found for this student.")  # Check if the student is enrolled in any course
        return

    print(f"\nEnrolled courses for {students[student_id]['Name']} ({student_id}):")
    for i, enrollment in enumerate(enrollments[student_id], 1):
        print(f"{i}. {courses[enrollment['CourseID']]['Name']} ({enrollment['CourseID']})")  # Show list of enrolled courses

    while True:
        try:
            choice = int(input("Enter the number of the course to drop: ").strip())  # Ask the user to select a course to drop
            if 1 <= choice <= len(enrollments[student_id]):
                break  # If valid choice, break the loop
            else:
                print("Invalid selection. Try again.")  # If the selection is invalid, prompt again
        except ValueError:
            print("Please enter a valid number.")  # If the input is not a number, prompt again

    dropped_course = enrollments[student_id].pop(choice - 1)  # Remove the selected course from enrollments
    courses[dropped_course['CourseID']]['Seats'] += 1  # Increase the available seats for the dropped course
    save_data()  # Save the updated data to the file
    print(f"Dropped {courses[dropped_course['CourseID']]['Name']} ({dropped_course['CourseID']}).")  # Inform the user

# Function to view available courses
def view_courses():
    if not courses:
        print("No courses available.")  # If no courses, inform the user
        return

    print("\nAvailable Courses:")
    print(f"{'Course ID':<10} {'Name':<25} {'Seats':<5}")  # Print table headers
    print("-" * 40)  # Print separator
    for course_id, course_info in courses.items():
        print(f"{course_id:<10} {course_info['Name']:<25} {course_info['Seats']:<5}")  # Print course details

# Function to view student information
def view_students():
    if not students:
        print("No students registered.")  # If no students, inform the user
        return

    print("\nRegistered Students:")
    print(f"{'ID':<10} {'Name':<20} {'Contact':<15}")  # Print table headers
    print("-" * 45)  # Print separator
    for student_id, student_info in students.items():
        print(f"{student_id:<10} {student_info['Name']:<20} {student_info['Contact']:<15}")  # Print student details

# Function to exit the program
def exit_program():
    while True:
        confirm = input("Are you sure you want to exit? (yes/no): ").strip().lower()  # Ask for confirmation to exit

        if confirm == "yes":
            retain_data = input("Do you want to retain existing data? (yes/no): ").strip().lower()  # Ask if user wants to retain data
            if retain_data == "yes":
                print("Exiting program. All stored data will be retained.")  # Inform the user that data will be retained
                break
            elif retain_data =="no":
                open("students.txt", "w").close()  # Clear the data by closing the file (i.e., delete its content)
                open("courses.txt", "w").close()
                open("enrollments.txt", "w").close()
                print("Exiting program. All stored data will be cleared.")  # Inform the user that data will be cleared
                break # Exit the loop and terminate the program
            else:
                print("Invalid input. Please choose yes or no.")
                continue # Ask again for retain data
        elif confirm == "no":
            print("Continuing the program...") # Let the user know the program will continue
            return display_menu() # Return to the main menu instead of breaking the loop
        else:
            print("Invalid input. Please choose yes or no.")
            continue # Ask again if invalid input
    exit()  # Exit the program

# Main menu function to display options
def display_menu():
    while True:
        print("\nCourse Registration System")
        print("1. Add A New Student")
        print("2. Add A New Course")
        print("3. View Available Courses")
        print("4. View Student Information")
        print("5. Enroll In A Course")
        print("6. Drop A Course")
        print("7. Exit")

        choice = input("Select an option: ").strip()  # Prompt the user to select an option
        if choice == "1":
            add_student()
        elif choice == "2":
            add_course()
        elif choice == "3":
            view_courses()
        elif choice == "4":
            view_students()
        elif choice == "5":
            enroll_in_course()
        elif choice == "6":
            drop_course()
        elif choice == "7":
            exit_program()  # Exit the program if option 7 is selected
            break
        else:
            print("Invalid option, try again.")  # Prompt the user to try again if the input is invalid

# Start the menu display
display_menu()
