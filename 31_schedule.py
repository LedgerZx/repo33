import json
from datetime import datetime, timedelta

# File to store the schedule
SCHEDULE_FILE = 'weekly_schedule.json'

# Load the existing schedule or create a new one
def load_schedule():
    try:
        with open(SCHEDULE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"events": []}

# Save the schedule to a file
def save_schedule(schedule):
    with open(SCHEDULE_FILE, 'w') as file:
        json.dump(schedule, file, indent=4)

# Add an event to the schedule
def add_event(schedule, day, time, description):
    event = {
        "day": day,
        "time": time,
        "description": description
    }
    schedule["events"].append(event)
    save_schedule(schedule)
    print(f"Event '{description}' added on {day} at {time}.")

# View the schedule
def view_schedule(schedule):
    if not schedule["events"]:
        print("No events in the schedule.")
        return
    for event in schedule["events"]:
        print(f"{event['day']} at {event['time']}: {event['description']}")

# Remove an event from the schedule
def remove_event(schedule, day, time):
    schedule["events"] = [event for event in schedule["events"] if not (event["day"] == day and event["time"] == time)]
    save_schedule(schedule)
    print(f"Event on {day} at {time} removed.")

# Main function to interact with the user
def main():
    schedule = load_schedule()
    while True:
        print("\nWeekly Schedule Menu:")
        print("1. Add Event")
        print("2. View Schedule")
        print("3. Remove Event")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            day = input("Enter the day (e.g., Monday): ")
            time = input("Enter the time (e.g., 10:00 AM): ")
            description = input("Enter the event description: ")
            add_event(schedule, day, time, description)

        elif choice == '2':
            view_schedule(schedule)

        elif choice == '3':
            day = input("Enter the day of the event to remove (e.g., Monday): ")
            time = input("Enter the time of the event to remove (e.g., 10:00 AM): ")
            remove_event(schedule, day, time)

        elif choice == '4':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
