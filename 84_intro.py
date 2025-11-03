def intro():
    print("Welcome to the Text Adventure Game!")
    print("You find yourself at the entrance of a dark forest.")
    print("There are two paths ahead of you.")
    print("1. Take the left path.")
    print("2. Take the right path.")
    choice = input("What do you do? (1 or 2): ")
    if choice == '1':
        left_path()
    elif choice == '2':
        right_path()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        intro()

def left_path():
    print("\nYou take the left path and walk deeper into the forest.")
    print("You come across a river. There is a bridge to your left and a raft to your right.")
    print("1. Cross the bridge.")
    print("2. Take the raft.")
    choice = input("What do you do? (1 or 2): ")
    if choice == '1':
        bridge()
    elif choice == '2':
        raft()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        left_path()

def right_path():
    print("\nYou take the right path and soon reach a clearing.")
    print("In the clearing, you see a mysterious cabin.")
    print("1. Approach the cabin.")
    print("2. Avoid the cabin and continue through the forest.")
    choice = input("What do you do? (1 or 2): ")
    if choice == '1':
        cabin()
    elif choice == '2':
        continue_forest()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        right_path()

def bridge():
    print("\nYou cross the bridge and reach the other side of the river.")
    print("You find a hidden treasure chest!")
    print("Congratulations! You've won the game!")
    play_again()

def raft():
    print("\nYou take the raft and cross the river.")
    print("Unfortunately, the raft tips over, and you fall into the water.")
    print("Game Over!")
    play_again()

def cabin():
    print("\nYou approach the cabin and knock on the door.")
    print("An old woman answers and invites you in for tea.")
    print("You spend a pleasant evening by the fire, sharing stories.")
    print("Congratulations! You've won the game!")
    play_again()

def continue_forest():
    print("\nYou avoid the cabin and continue through the forest.")
    print("You get lost and can't find your way back.")
    print("Game Over!")
    play_again()

def play_again():
    choice = input("Do you want to play again? (yes or no): ")
    if choice.lower() == 'yes':
        intro()
    elif choice.lower() == 'no':
        print("Thank you for playing!")
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")
        play_again()

# Start the game
intro()
