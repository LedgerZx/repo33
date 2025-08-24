import random
import time

# Define activities and their durations in minutes
activities = {
    "Wake Up": 10,
    "Breakfast": 20,
    "Work/Study": 480,  # 8 hours
    "Lunch": 30,
    "Relaxation": 60,
    "Dinner": 30,
    "Hobby": 60,
    "Sleep Preparation": 30,
    "Sleep": 480  # 8 hours
}

# Simulate a day
def simulate_day():
    for activity, duration in activities.items():
        print(f"\nStarting: {activity}")
        time.sleep(duration)  # Simulate the passage of time
        print(f"Finished: {activity}")

# Add random events to the day
def add_random_events():
    random_events = [
        "Unexpected visitor",
        "Rainy day",
        "Traffic jam",
        "Surprise party",
        "Unexpected meeting"
    ]
    for _ in range(2):  # Add 2 random events
        event = random.choice(random_events)
        print(f"\nRandom Event: {event}")
        time.sleep(10)  # Simulate time spent on the event

# Main function to run the simulation
def main():
    print("Starting the simulation of a day...")
    simulate_day()
    add_random_events()
    print("\nEnd of the simulated day.")

if __name__ == "__main__":
    main()
