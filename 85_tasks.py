import json
import os

TASK_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, task):
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added: {task}')

def view_tasks(tasks):
    if not tasks:
        print("Your to-do list is empty.")
    else:
        print("Your to-do list:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def remove_task(tasks, task_number):
    if 1 <= task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f'Task removed: {removed_task}')
    else:
        print("Invalid task number.")

def main():
    tasks = load_tasks()
    while True:
        print("\nTo-Do List Application")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Remove a task")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            task = input("Enter the task: ")
            add_task(tasks, task)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            try:
                task_number = int(input("Enter the task number to remove: "))
                remove_task(tasks, task_number)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
