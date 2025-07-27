import random
import string

def generate_password(length=12, use_lower=True, use_upper=True, use_digits=True, use_symbols=True):
    char_pool = ''
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += '!@#$%^&*()'
    
    if not char_pool:
        return "Error: No character types selected!"
    
    password = ''.join(random.choices(char_pool, k=length))
    return password

def check_strength(password):
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in '!@#$%^&*()' for c in password):
        strength += 1
    
    common_passwords = ["password", "123456", "qwerty", "abc123"]
    if password in common_passwords:
        return "Very Weak (common password)"
    
    if strength <= 2:
        return "Weak"
    elif strength == 3:
        return "Moderate"
    elif strength == 4:
        return "Strong"
    else:
        return "Very Strong"

def main():
    saved_passwords = {}
    while True:
        print("\n--- Password Generator ---")
        print("1. Generate new password")
        print("2. Check password strength")
        print("3. View saved passwords")
        print("4. Exit")
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            try:
                length = int(input("Enter password length (default 12): ") or 12)
                if length < 1:
                    print("Invalid length")
                    continue
                    
                use_lower = input("Include lowercase? (y/n): ").lower() == 'y'
                use_upper = input("Include uppercase? (y/n): ").lower() == 'y'
                use_digits = input("Include numbers? (y/n): ").lower() == 'y'
                use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
                
                password = generate_password(length, use_lower, use_upper, use_digits, use_symbols)
                print(f"\nGenerated password: {password}")
                print(f"Strength: {check_strength(password)}")
                
                if input("Save this password? (y/n): ").lower() == 'y':
                    label = input("Enter label for password: ")
                    saved_passwords[label] = password
                    print("Password saved!")
                    
            except ValueError:
                print("Invalid input for length")
                
        elif choice == '2':
            pwd = input("Enter password to check: ")
            print(f"Strength: {check_strength(pwd)}")
            
        elif choice == '3':
            if not saved_passwords:
                print("No passwords saved yet")
            else:
                print("\nSaved Passwords:")
                for label, pwd in saved_passwords.items():
                    print(f"{label}: {pwd} ({check_strength(pwd)})")
                    
        elif choice == '4':
            print("Goodbye!")
            break
            
        else:
            print("Invalid option selected")

if __name__ == "__main__":
    main()
