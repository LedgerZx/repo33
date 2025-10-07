class Room:
    def __init__(self, name, description, items=None, exits=None):
        self.name = name
        self.description = description
        self.items = items if items is not None else []
        self.exits = exits if exits is not None else {}

    def describe(self):
        print(f"\nYou are in the {self.name}.")
        print(self.description)
        if self.items:
            print("You see the following items: " + ", ".join(self.items))
        if self.exits:
            print("Exits: " + ", ".join(self.exits.keys()))

    def move(self, direction):
        if direction in self.exits:
            return self.exits[direction]
        else:
            print("You can't go that way.")
            return self

class Game:
    def __init__(self):
        self.rooms = {}
        self.current_room = None
        self.inventory = []

    def add_room(self, room):
        self.rooms[room.name] = room

    def start(self, starting_room):
        self.current_room = self.rooms[starting_room]
        self.current_room.describe()
        self.play()

    def play(self):
        while True:
            command = input("> ").strip().lower()
            if command in ["north", "south", "east", "west"]:
                self.current_room = self.current_room.move(command)
                self.current_room.describe()
            elif command.startswith("take "):
                item = command[5:]
                if item in self.current_room.items:
                    self.current_room.items.remove(item)
                    self.inventory.append(item)
                    print(f"You have taken the {item}.")
                else:
                    print("There is no such item here.")
            elif command == "inventory":
                if self.inventory:
                    print("You are carrying: " + ", ".join(self.inventory))
                else:
                    print("You are not carrying anything.")
            elif command == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Unknown command.")

# Create rooms
hallway = Room("Hallway", "A long, dimly lit hallway.")
kitchen = Room("Kitchen", "A cozy kitchen with a wooden table.", items=["knife", "apple"])
bedroom = Room("Bedroom", "A small bedroom with a single bed.", items=["book"])
garden = Room("Garden", "A beautiful garden with colorful flowers.", items=["flower"])

# Define exits
hallway.exits = {"north": kitchen, "east": bedroom}
kitchen.exits = {"south": hallway, "west": garden}
bedroom.exits = {"west": hallway}
garden.exits = {"east": kitchen}

# Create game and add rooms
game = Game()
game.add_room(hallway)
game.add_room(kitchen)
game.add_room(bedroom)
game.add_room(garden)

# Start the game
game.start("Hallway")
