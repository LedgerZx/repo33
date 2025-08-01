import re
from collections import Counter

def read_file(file_path):
    """Reads the content of a file and returns it as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def count_words(text):
    """Counts the frequency of each word in the given text."""
    # Use regex to find all words, ignoring case and punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def write_word_count(file_path, word_count):
    """Writes the word count to a new file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for word, count in word_count.items():
                file.write(f"{word}: {count}\n")
        print(f"Word count has been written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")

def main():
    input_file = 'input.txt'  # Replace with your input file path
    output_file = 'word_count.txt'  # Replace with your desired output file path

    # Read the content of the input file
    text = read_file(input_file)
    if text is None:
        return

    # Count the words in the text
    word_count = count_words(text)

    # Write the word count to the output file
    write_word_count(output_file, word_count)

if __name__ == "__main__":
    main()
