import logging
from app.exceptions.exceptions import InvalidInputError
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NumberService:
    def check_even_odd(self, num):
        if self.is_even(num):
            return f"{num} is even."
        else:
            return f"{num} is odd."

    def is_even(self, num):
        return num % 2 == 0

    def factorial(self, num):
        if num < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        result = 1
        while num > 1:
            result *= num
            num -= 1
        return result

    def process_numbers(self, numbers):
        results = []
        for num in numbers:
            if not self.is_integer(num):
                logging.error(f"Invalid input for integer: {num}")
                raise InvalidInputError("Invalid input. Expected an integer", num)
            if self.is_even(int(num)):
                results.append(f"{num} is even.")
            else:
                results.append(f"{num} is odd.")
        return results

    def is_integer(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
