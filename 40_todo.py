import os

TODO_FILE = 'todo.txt'

def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def show_tasks(tasks):
    if not tasks:
        print("Your todo list is empty!")
    else:
        print("Your todo list:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def main():
    tasks = load_tasks()

    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. View tasks")
        print("3. Remove task")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            task = input("Enter the task: ")
            tasks.append(task)
            save_tasks(tasks)
            print("Task added!")

        elif choice == '2':
            show_tasks(tasks)

        elif choice == '3':
            show_tasks(tasks)
            try:
                task_number = int(input("Enter the number of the task to remove: "))
                if 1 <= task_number <= len(tasks):
                    removed_task = tasks.pop(task_number - 1)
                    save_tasks(tasks)
                    print(f"Task removed: {removed_task}")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            print("Exiting the todo list application.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
