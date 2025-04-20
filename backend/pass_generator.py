import random
import string

class PasswordGenerator:
    """
    A class to generate secure passwords based on user-defined criteria.
    """

    def __init__(self):
        self.maxlen = 12
        self.minuchars = 0  # Minimum uppercase characters
        self.minlchars = 0  # Minimum lowercase characters
        self.minnumbers = 0  # Minimum numeric characters
        self.minschars = 0  # Minimum special characters

    def generate(self):
        """
        Generate a password based on the configured criteria.
        """
        if self.maxlen < self.minuchars + self.minlchars + self.minnumbers + self.minschars:
            raise ValueError("Password length is too short for the given criteria.")

        # Character pools
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        numbers = string.digits
        special = "!@#$%"  # Restrict special characters to this pool

        # Build the password and character pool dynamically
        password = []
        all_chars = ""

        if self.minuchars > 0:
            password += random.choices(upper, k=self.minuchars)
            all_chars += upper

        if self.minlchars > 0:
            password += random.choices(lower, k=self.minlchars)
            all_chars += lower

        if self.minnumbers > 0:
            password += random.choices(numbers, k=self.minnumbers)
            all_chars += numbers

        if self.minschars > 0:
            password += random.choices(special, k=self.minschars)
            all_chars += special

        # Fill the rest of the password length with random characters from the selected pools
        remaining_length = self.maxlen - len(password)
        if remaining_length > 0:
            password += random.choices(all_chars, k=remaining_length)

        # Shuffle the password to ensure randomness
        random.shuffle(password)
        return ''.join(password)

    def calculate_strength(self, password):
        """
        Calculate the strength of a password based on its length and character variety.
        """
        length = len(password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_number = any(char.isdigit() for char in password)
        has_special = any(char in "!@#$%" for char in password)

        # Assign points based on criteria
        score = 0
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_number:
            score += 1
        if has_special:
            score += 1
        if length >= 12:
            score += 1

        # Determine strength based on score
        if score <= 2:
            return "Weak"
        elif score == 3:
            return "Okay"
        elif score == 4:
            return "Strong"
        else:
            return "Very Strong"

# Example usage (remove this if not needed):
if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.maxlen = 12
    generator.minuchars = 2
    generator.minlchars = 4
    generator.minnumbers = 3
    generator.minschars = 2
    password = generator.generate()
    print(f"Generated Password: {password}")
    print(f"Password Strength: {generator.calculate_strength(password)}")