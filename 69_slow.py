def print_slow(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_user_choice(prompt, options):
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        else:
            print("Invalid choice. Please choose a valid option.")

def main():
    print_slow("Welcome to the Enchanted Forest Adventure!")
    print_slow("You find yourself at the edge of a mysterious forest. What would you like to do?")
    print("1. Enter the forest")
    print("2. Walk along the forest's edge")

    choice = get_user_choice("Enter your choice (1/2): ", ["1", "2"])

    if choice == "1":
        print_slow("You bravely step into the forest. The trees are dense, and the path is unclear.")
        print_slow("As you venture deeper, you hear a faint sound in the distance. What do you do?")
        print("1. Follow the sound")
        print("2. Ignore the sound and continue straight")

        choice = get_user_choice("Enter your choice (1/2): ", ["1", "2"])

        if choice == "1":
            print_slow("You follow the sound and discover a hidden waterfall with a crystal-clear pool.")
            print_slow("The water shimmers with a magical aura. You feel refreshed and invigorated.")
            print_slow("Congratulations! You have found the Enchanted Waterfall, a place of peace and wonder.")
        else:
            print_slow("You ignore the sound and continue straight. The path becomes increasingly difficult.")
            print_slow("Eventually, you find yourself lost and exhausted. You decide to turn back.")
            print_slow("As you retrace your steps, you realize the importance of listening to your instincts.")

    else:
        print_slow("You decide to walk along the forest's edge. The sun is warm, and the birds are singing.")
        print_slow("After a while, you come across a small cottage with smoke rising from the chimney.")
        print_slow("You approach the cottage and knock on the door. An old woman answers, smiling warmly.")
        print_slow("She invites you in and offers you a cup of tea. You spend the afternoon listening to her tales of the forest.")
        print_slow("Thank you for joining the Enchanted Forest Adventure! We hope you enjoyed your journey.")

if __name__ == "__main__":
    import time
    main()
