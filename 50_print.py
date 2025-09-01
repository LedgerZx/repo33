import time

def print_slow(text, delay=0.05):
    """Prints text slowly, character by character."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_choice(prompt, options):
    """Prompts the user to make a choice from a list of options."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")

def main():
    print_slow("Welcome to the Mysterious Forest Adventure!")
    print_slow("You find yourself at the edge of a dense, eerie forest. Your goal is to uncover the forest's secret.")
    print()

    # Start the adventure
    print_slow("You stand at the entrance of the forest. There are two paths ahead.")
    choice = get_choice("Do you want to take the left path (L) or the right path (R)? ", ['l', 'r'])

    if choice == 'l':
        print_slow("You take the left path and walk deeper into the forest. After a while, you hear whispers.")
        print_slow("Suddenly, a ghostly figure appears before you, asking for your help to lift a curse.")
        print_slow("The ghost reveals that the forest is cursed and only you can break it by finding the hidden amulet.")
        print_slow("You agree to help and continue your journey, determined to find the amulet and break the curse.")
    else:
        print_slow("You take the right path and soon come across an ancient, crumbling stone bridge.")
        print_slow("Crossing the bridge, you discover a hidden cave entrance. Inside, you find a mysterious map.")
        print_slow("The map leads you to a hidden chamber where you find the amulet, but also realize you are not alone.")
        print_slow("You must now decide whether to confront the mysterious presence or flee the cave with the amulet.")

    # Ending
    print_slow("Congratulations! You have uncovered the secret of the Mysterious Forest!")
    print_slow("Thank you for playing the adventure game. Your choices led you on an exciting journey!")

if __name__ == "__main__":
    main()
