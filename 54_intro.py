def print_intro():
    print("Welcome to the Adventure Game!")
    print("You find yourself standing at the entrance of a mysterious forest.")
    print("There are two paths ahead of you.")
    print("1. Take the left path.")
    print("2. Take the right path.")
    print("What do you do? (Enter 1 or 2)")

def left_path():
    print("\nYou take the left path and walk deeper into the forest.")
    print("After a while, you come across a small cottage.")
    print("1. Knock on the door.")
    print("2. Peek through the window.")
    print("What do you do? (Enter 1 or 2)")

def right_path():
    print("\nYou take the right path and soon encounter a crossroads.")
    print("There are three paths ahead.")
    print("1. Take the path to the north.")
    print("2. Take the path to the east.")
    print("3. Take the path to the west.")
    print("What do you do? (Enter 1, 2, or 3)")

def cottage_door():
    print("\nYou knock on the door, and an old woman answers.")
    print("She invites you inside and offers you a cup of tea.")
    print("You spend the evening listening to her stories about the forest.")
    print("You decide to rest for the night and continue your journey in the morning.")

def cottage_window():
    print("\nYou peek through the window and see an old woman sitting by the fire.")
    print("She seems to be waiting for someone.")
    print("You decide to continue your journey and leave the cottage behind.")

def north_path():
    print("\nYou take the path to the north and soon reach a river.")
    print("There is a bridge, but it looks old and rickety.")
    print("1. Cross the bridge.")
    print("2. Follow the river to find a safer crossing.")
    print("What do you do? (Enter 1 or 2)")

def east_path():
    print("\nYou take the path to the east and soon reach a clearing.")
    print("In the middle of the clearing, there is a magical tree.")
    print("You decide to rest under the tree and feel rejuvenated.")
    print("You continue your journey, feeling refreshed and energized.")

def west_path():
    print("\nYou take the path to the west and soon reach a cave.")
    print("The entrance is dark, and you can't see what's inside.")
    print("1. Enter the cave.")
    print("2. Decide to explore another path.")
    print("What do you do? (Enter 1 or 2)")

def cave_enter():
    print("\nYou enter the cave and discover a hidden treasure.")
    print("You take the treasure and decide to return to the surface.")
    print("You continue your journey, feeling rich and satisfied.")

def bridge_cross():
    print("\nYou carefully cross the bridge and reach the other side.")
    print("You continue your journey, feeling proud of your bravery.")

def river_follow():
    print("\nYou follow the river and find a safer crossing point.")
    print("You cross the river and continue your journey, feeling relieved.")

def main():
    print_intro()
    choice = input("> ")

    if choice == '1':
        left_path()
        choice = input("> ")
        if choice == '1':
            cottage_door()
        elif choice == '2':
            cottage_window()
    elif choice == '2':
        right_path()
        choice = input("> ")
        if choice == '1':
            north_path()
            choice = input("> ")
            if choice == '1':
                bridge_cross()
            elif choice == '2':
                river_follow()
        elif choice == '2':
            east_path()
        elif choice == '3':
            west_path()
            choice = input("> ")
            if choice == '1':
                cave_enter()
            elif choice == '2':
                print("\nYou decide to explore another path and continue your journey.")

if __name__ == "__main__":
    main()
