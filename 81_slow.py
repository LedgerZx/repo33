import time

def print_slow(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def adventure_game():
    print_slow("Welcome to the Text Adventure Game!")
    print_slow("You find yourself at the entrance of a mysterious forest.")
    print_slow("You have two paths ahead of you. One leads to the left, the other to the right.")
    choice = input("Which path do you choose? (left/right): ").strip().lower()

    if choice == 'left':
        print_slow("You walk down the left path and come across a small cottage.")
        print_slow("Inside the cottage, you see an old woman sitting by the fire.")
        print_slow("She offers you a cup of tea and asks if you would like to hear a story.")
        story_choice = input("Do you accept her offer? (yes/no): ").strip().lower()
        if story_choice == 'yes':
            print_slow("The old woman begins to tell you a fascinating tale of ancient heroes and magical creatures.")
            print_slow("You spend the night in the cottage, feeling enriched by the experience.")
        else:
            print_slow("You politely decline and continue your journey through the forest.")
            print_slow("The path leads you to a beautiful meadow with wildflowers.")
    elif choice == 'right':
        print_slow("You take the right path and soon hear the sound of rushing water.")
        print_slow("You discover a hidden waterfall and a crystal-clear pool.")
        print_slow("The sight is breathtaking, and you decide to rest by the pool.")
        rest_choice = input("Do you want to take a dip in the pool? (yes/no): ").strip().lower()
        if rest_choice == 'yes':
            print_slow("You take a refreshing dip in the pool, feeling rejuvenated.")
        else:
            print_slow("You sit by the pool, enjoying the tranquility of the moment.")
    else:
        print_slow("Invalid choice. Please choose 'left' or 'right'.")

    print_slow("Thank you for playing the Text Adventure Game!")
    print_slow("Your choices shaped your journey. Until next time, adventurer!")

if __name__ == "__main__":
    adventure_game()
