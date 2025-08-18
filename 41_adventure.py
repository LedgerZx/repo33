import time

def print_slow(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def adventure_game():
    print_slow("Welcome to the Magical Forest Adventure!")
    print_slow("You find yourself at the edge of a mysterious forest. Your goal is to reach the magical tree at the center and retrieve a legendary artifact.")
    print_slow("Let's begin your journey!")

    while True:
        print_slow("You are at a crossroads. Do you want to go left or right?")
        choice = input("Enter 'left' or 'right': ").lower()

        if choice == 'left':
            print_slow("You take the path to the left. The forest becomes dense, and you hear strange noises.")
            print_slow("Suddenly, a friendly talking fox appears!")
            print_slow("Fox: 'Greetings, traveler! I am the guardian of this path. Answer my riddle, and I shall grant you safe passage.'")
            print_slow("Riddle: 'I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?")
            answer = input("Your answer: ").lower()

            if answer == 'echo':
                print_slow("The fox smiles and says, 'Well done! You may pass.'")
                print_slow("You continue your journey and eventually reach the magical tree. Congratulations!")
                break
            else:
                print_slow("The fox shakes its head. 'Incorrect! You must find another way.'")
                continue

        elif choice == 'right':
            print_slow("You take the path to the right. The forest is beautiful, with vibrant flowers and gentle streams.")
            print_slow("You come across a wise old owl perched on a branch.")
            print_slow("Owl: 'Welcome, traveler. I sense you seek the magical tree. I can guide you, but you must answer my question first.'")
            print_slow("Question: 'What is the one thing that all wise people, regardless of their culture or beliefs, agree upon?'")
            answer = input("Your answer: ").lower()

            if answer == 'knowledge':
                print_slow("The owl nods approvingly. 'You are wise indeed. Follow this path, and you shall reach your destination.'")
                print_slow("You follow the owl's advice and reach the magical tree. Congratulations!")
                break
            else:
                print_slow("The owl looks disappointed. 'Think deeply, and try again.'")
                continue

        else:
            print_slow("Invalid choice. Please enter 'left' or 'right'.")

if __name__ == "__main__":
    adventure_game()
