import random
import string

def generate_password(length=12):
    if length < 6:
        raise ValueError("Password length should be at least 6 characters.")

    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Ensure password has at least one of each
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Fill the rest of the password length
    all_chars = letters + digits + symbols
    password += random.choices(all_chars, k=length - 3)

    # Shuffle to prevent predictable pattern
    random.shuffle(password)

    return ''.join(password)

# Example usage
if __name__ == "__main__":
    print("Your generated password is:", generate_password(16))
