class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

class School:
    def __init__(self):
        self.students = []

    def add_student(self, name, age, grade):
        new_student = Student(name, age, grade)
        self.students.append(new_student)
        print(f"Student {name} added successfully.")

    def display_students(self):
        if not self.students:
            print("No students in the school.")
        else:
            for student in self.students:
                print(f"Name: {student.name}, Age: {student.age}, Grade: {student.grade}")

    def search_student(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                print(f"Student found: Name: {student.name}, Age: {student.age}, Grade: {student.grade}")
                return
        print(f"No student found with the name {name}.")

# Example usage
if __name__ == "__main__":
    school = School()

    while True:
        print("\nSchool Management System")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student by Name")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            age = input("Enter student age: ")
            grade = input("Enter student grade: ")
            school.add_student(name, age, grade)
        elif choice == '2':
            school.display_students()
        elif choice == '3':
            name = input("Enter student name to search: ")
            school.search_student(name)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
