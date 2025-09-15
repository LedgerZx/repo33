import random
import time

# Define the colors and their corresponding words
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
words = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'PURPLE', 'ORANGE']

# Function to display a word in a specific color
def display_word(word, color):
    print(f"\033[9{color}m{word}\033[0m")

# Function to conduct the Stroop test
def stroop_test():
    print("Welcome to the Stroop Effect Test!")
    print("You will see a series of colored words. Your task is to name the color of the word, not read the word itself.")
    input("Press Enter to begin...")

    # Randomly select words and colors
    test_words = [random.choice(words) for _ in range(10)]
    test_colors = [random.choice(colors) for _ in range(10)]

    # Conduct the test
    start_time = time.time()
    for word, color in zip(test_words, test_colors):
        display_word(word, colors.index(color) + 1)  # Convert color index to ANSI color code
        user_input = input("What color is the word? (type the color name): ").strip().lower()
        if user_input == color:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was {color}.")
    end_time = time.time()

    # Calculate and display the results
    duration = end_time - start_time
    print(f"\nTest completed in {duration:.2f} seconds.")
    print("Thank you for participating in the Stroop Effect Test!")

# Run the Stroop test
stroop_test()
