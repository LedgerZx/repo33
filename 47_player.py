import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []

    def show_status(self):
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print()

def start_game():
    print("Welcome to the Adventure Game!")
    player_name = input("Enter your name: ")
    player = Player(player_name)
    print(f"Hello, {player.name}! Let's begin your adventure.\n")

    while player.health > 0:
        print("You are in a mysterious forest. Choose your path:")
        print("1. Go left")
        print("2. Go right")
        print("3. Check your inventory")
        print("4. Quit the game")
        choice = input("> ")

        if choice == "1":
            encounter(player, "left")
        elif choice == "2":
            encounter(player, "right")
        elif choice == "3":
            player.show_status()
        elif choice == "4":
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.\n")

def encounter(player, direction):
    if direction == "left":
        if random.choice([True, False]):
            print("You found a healing potion!")
            player.inventory.append("Healing Potion")
            player.health = min(100, player.health + 20)
        else:
            print("You encountered a wild beast and lost 10 health!")
            player.health -= 10
    elif direction == "right":
        if random.choice([True, False]):
            print("You found a treasure chest!")
            player.inventory.append("Treasure")
        else:
            print("You tripped and fell, losing 5 health!")
            player.health -= 5
    print()

if __name__ == "__main__":
    start_game()
