
import random
import string

# Function to generate a random password
def generate_password(length=12):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to check password strength
def check_password_strength(password):
    length_ok = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    strength = sum([length_ok, has_upper, has_lower, has_digit, has_special])
    return strength

# Function to get user input for password generation
def get_user_input():
    print("Welcome to the Password Generator!")
    length = int(input("Enter the desired length of the password: "))
    return length

# Main function to run the password generator
def main():
    length = get_user_input()
    password = generate_password(length)
    print(f"Generated Password: {password}")
    strength = check_password_strength(password)
    if strength == 5:
        print("Password strength: Strong")
    elif strength == 4:
        print("Password strength: Medium")
    else:
        print("Password strength: Weak")

# Run the main function
if __name__ == "__main__":
    main()

# Function to encrypt a message using a simple Caesar cipher
def caesar_cipher_encrypt(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            encrypted_char = chr((ord(char) - shift_amount + shift) % 26 + shift_amount)
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message

# Function to decrypt a message using a simple Caesar cipher
def caesar_cipher_decrypt(encrypted_message, shift):
    return caesar_cipher_encrypt(encrypted_message, -shift)

# Function to get user input for encryption/decryption
def get_cipher_input():
    choice = input("Do you want to encrypt or decrypt a message? (e/d): ").lower()
    message = input("Enter the message: ")
    shift = int(input("Enter the shift value: "))
    return choice, message, shift

# Main function to run the Caesar cipher
def cipher_main():
    choice, message, shift = get_cipher_input()
    if choice == 'e':
        result = caesar_cipher_encrypt(message, shift)
        print(f"Encrypted Message: {result}")
    elif choice == 'd':
        result = caesar_cipher_decrypt(message, shift)
        print(f"Decrypted Message: {result}")
    else:
        print("Invalid choice. Please enter 'e' for encrypt or 'd' for decrypt.")

# Run the cipher main function
if __name__ == "__main__":
    cipher_main()

# Function to generate a random quote
def generate_quote():
    quotes = [
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
    ]
    return random.choice(quotes)

# Function to get user input for quote generation
def get_quote_input():
    print("Welcome to the Quote Generator!")
    input("Press Enter to generate a random quote: ")

# Main function to run the quote generator
def quote_main():
    get_quote_input()
    quote = generate_quote()
    print(f"Random Quote: {quote}")

# Run the quote main function
if __name__ == "__main__":
    quote_main()
