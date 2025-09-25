import random

# Define the rooms and their connections
rooms = {
    "Entrance": {
        "description": "You are at the entrance of a mysterious castle. There are doors to the north and east.",
        "exits": {"north": "Hallway", "east": "Library"},
        "items": []
    },
    "Hallway": {
        "description": "You are in a long hallway. There are doors to the south and west.",
        "exits": {"south": "Entrance", "west": "Dungeon"},
        "items": ["sword"]
    },
    "Library": {
        "description": "You are in a vast library filled with ancient books. There is a door to the west.",
        "exits": {"west": "Entrance"},
        "items": ["map"]
    },
    "Dungeon": {
        "description": "You are in a dark dungeon. There is a door to the east. You hear a growl in the distance.",
        "exits": {"east": "Hallway"},
        "items": ["key"]
    }
}

# Function to display the current room
def show_room(room):
    print("\n" + room["description"])
    if room["items"]:
        print("You see the following items: " + ", ".join(room["items"]))
    print("Exits: " + ", ".join(room["exits"].keys()))

# Function to handle player movement
def move_room(current_room, direction):
    if direction in current_room["exits"]:
        return current_room["exits"][direction]
    else:
        print("You can't go that way.")
        return current_room

# Function to handle item collection
def collect_item(room, item):
    if item in room["items"]:
        room["items"].remove(item)
        print(f"You have collected a {item}.")
        return item
    else:
        print(f"There is no {item} here.")
        return None

# Game loop
current_room = rooms["Entrance"]
inventory = []

while True:
    show_room(current_room)

    command = input("What do you do? ").strip().lower()

    if command in ["north", "south", "east", "west"]:
        current_room = move_room(current_room, command)
    elif command.startswith("take "):
        item = command[5:]
        collect_item(current_room, item)
    elif command == "inventory":
        if inventory:
            print("You have: " + ", ".join(inventory))
        else:
            print("Your inventory is empty.")
    elif command in ["quit", "exit"]:
        print("Thanks for playing!")
        break
    else:
        print("Invalid command. Try 'north', 'south', 'east', 'west', 'take item', or 'inventory'.")

# End of the game
