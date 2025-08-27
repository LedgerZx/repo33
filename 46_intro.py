def print_intro():
    print("Welcome to the Adventure Game!")
    print("You find yourself in a dark forest. You have three paths in front of you.")
    print("1. The path to the left leads to a mysterious cave.")
    print("2. The path straight ahead leads to a dense thicket.")
    print("3. The path to the right leads to a sparkling river.")

def get_choice():
    choice = input("Which path do you choose? (1, 2, or 3): ")
    return choice

def path_one():
    print("You enter the mysterious cave. It's damp and dark.")
    print("You see a glimmer of light ahead. As you approach, you discover a hidden treasure chest!")
    print("Congratulations! You found the treasure!")

def path_two():
    print("You venture into the dense thicket. The branches scratch your skin.")
    print("Suddenly, you hear a rustling sound. It's a wild boar!")
    print("You run as fast as you can, escaping just in time. Phew, that was close!")

def path_three():
    print("You walk towards the sparkling river. The water looks inviting.")
    print("You decide to take a dip. The water is refreshing and cool.")
    print("You spend a peaceful afternoon by the river, enjoying the nature around you.")

def main():
    print_intro()
    choice = get_choice()
    if choice == '1':
        path_one()
    elif choice == '2':
        path_two()
    elif choice == '3':
        path_three()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
