class Room:
    def __init__(self, name, description, items, connections):
        self.name = name
        self.description = description
        self.items = items
        self.connections = connections

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)
        print(f"You picked up: {item}")

    def use_item(self, item):
        if item in self.inventory:
            print(f"You used: {item}")
            self.inventory.remove(item)
        else:
            print(f"You don't have {item} in your inventory.")

def create_world():
    # Create rooms
    entrance = Room("Entrance", "You are at the entrance of a mysterious cave.", ["torch"], {"north": "hallway"})
    hallway = Room("Hallway", "A long, dimly lit hallway stretches before you.", ["key"], {"south": "entrance", "east": "treasure room"})
    treasure_room = Room("Treasure Room", "A room filled with gold and jewels!", ["diamond"], {"west": "hallway"})

    # Create world
    world = {
        "entrance": entrance,
        "hallway": hallway,
        "treasure room": treasure_room
    }
    return world

def main():
    print("Welcome to the Text Adventure Game!")
    player_name = input("What is your name, adventurer? ")
    player = Player(player_name)
    world = create_world()
    current_room = world["entrance"]

    while True:
        print(f"\n{current_room.name}")
        print(current_room.description)
        if current_room.items:
            print(f"You see: {', '.join(current_room.items)}")

        command = input("\nWhat would you like to do? (go, take, use, quit) ").strip().lower()

        if command == "quit":
            print("Thanks for playing!")
            break
        elif command.startswith("go "):
            direction = command[3:]
            if direction in current_room.connections:
                current_room = world[current_room.connections[direction]]
            else:
                print("You can't go that way!")
        elif command.startswith("take "):
            item = command[5:]
            if item in current_room.items:
                player.add_item(item)
                current_room.items.remove(item)
            else:
                print(f"There is no {item} here.")
        elif command.startswith("use "):
            item = command[4:]
            player.use_item(item)
        else:
            print("I don't understand that command.")

if __name__ == "__main__":
    main()
