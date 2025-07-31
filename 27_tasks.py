import os
import json

# File to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file or create empty list"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(tasks):
    """Add a new task to the list"""
    description = input("Enter task description: ")
    tasks.append({"description": description, "completed": False})
    print("Task added successfully!")

def view_tasks(tasks):
    """Display all tasks with their status"""
    if not tasks:
        print("No tasks found!")
        return
    
    print("\nYour Tasks:")
    for i, task in enumerate(tasks):
        status = "✓" if task["completed"] else "✗"
        print(f"{i+1}. [{status}] {task['description']}")

def delete_task(tasks):
    """Delete a task by index"""
    if not tasks:
        print("No tasks to delete!")
        return
    
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            print(f"Deleted task: {removed['description']}")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def mark_complete(tasks):
    """Mark a task as completed"""
    if not tasks:
        print("No tasks to mark!")
        return
    
    try:
        index = int(input("Enter task number to mark as complete: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            print(f"Marked task as complete: {tasks[index]['description']}")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def main():
    """Main program loop"""
    tasks = load_tasks()
    
    while True:
        print("\n--- To-Do List Manager ---")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Mark Task as Complete")
        print("5. Save and Exit")
        
        choice = input("Select option (1-5): ")
        
        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            mark_complete(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Tasks saved. Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
