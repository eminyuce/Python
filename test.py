import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Service layer
class NumberService:
    def check_even_odd(self, num):
        if num % 2 == 0:
            return f"{num} is even."
        else:
            return f"{num} is odd."

    def factorial(self, num):
        if num < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        result = 1
        while num > 1:
            result *= num
            num -= 1
        return result

class StringService:
    def print_characters(self, string):
        for char in string:
            print(char)

# Controller layer
class MainController:
    def __init__(self, number_service, string_service):
        self.number_service = number_service
        self.string_service = string_service

    def run(self):
        try:
            # Get user input
            num_input = input("Enter an integer: ")
            try:
                num = int(num_input)
            except ValueError as ve:
                logging.error(f"Invalid input for integer: {num_input}")
                raise ValueError(f"Invalid input. Expected an integer, got '{num_input}'") from ve

            string = input("Enter a string: ")

            # Check if the number is even or odd using the NumberService
            even_odd_result = self.number_service.check_even_odd(num)
            print(even_odd_result)
            logging.info(f"Checked if {num} is even or odd.")

            # Calculate and print the factorial of the number using the NumberService
            factorial_result = self.number_service.factorial(num)
            print(f"The factorial of {num} is {factorial_result}.")
            logging.info(f"Calculated factorial of {num}.")

            # Print each character of the string using the StringService
            print(f"The characters in the string '{string}' are:")
            self.string_service.print_characters(string)
            logging.info(f"Printed characters of the string '{string}'.")

        except ValueError as e:
            print(f"Error: {e}")
            logging.error(f"ValueError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logging.error(f"Unexpected error: {e} for inputs num: {num_input}, string: '{string}'")

# Dependency injection and running the controller
if __name__ == "__main__":
    number_service = NumberService()
    string_service = StringService()
    controller = MainController(number_service, string_service)
    controller.run()
