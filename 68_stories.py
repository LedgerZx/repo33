import random

# Define a list of story templates
stories = [
    "Once upon a time, there was a {adjective} {noun} who lived in a {adjective} {place}. Every day, the {noun} would go on an adventure to find the {adjective} {noun}.",
    "In a far-off land, a brave {noun} set out on a quest to save the {adjective} {noun} from the clutches of the {adjective} {noun}.",
    "A {adjective} {animal} decided to {verb} across the {adjective} {place} to find the {adjective} {noun}. Along the way, it encountered a {adjective} {noun} who offered to help.",
    "The {adjective} {noun} woke up one morning to find that its {adjective} {noun} had been stolen by a mischievous {noun}. It had to {verb} to get it back.",
    "A group of {adjective} {plural_noun} decided to {verb} through the {adjective} {place} to discover the secrets of the {adjective} {noun}."
]

# Function to get user input for a specific part of speech
def get_input(part_of_speech):
    return input(f"Enter a {part_of_speech}: ")

# Main function to generate the story
def generate_story():
    # Randomly select a story template
    selected_story = random.choice(stories)
    print("You have chosen the following story template:")
    print(selected_story)
    print("\n")

    # Replace placeholders with user input
    for part_of_speech in ["adjective", "noun", "place", "animal", "verb", "plural_noun"]:
        selected_story = selected_story.replace(f"{{{part_of_speech}}}", get_input(part_of_speech))

    # Print the final story
    print("\nYour generated story is:")
    print(selected_story)

# Run the story generator
generate_story()
