import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Service layer
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
                raise ValueError(f"Invalid input. Expected an integer, got '{num}'")
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

class StringService:
    def print_characters(self, string):
        for char in string:
            print(char)

class ModelService:
    def __init__(self, file_path):
        self.file_path = file_path

    def filter_and_sort_models(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            
            # Filter models with age > 60
            filtered_models = [model for model in data if model.get('age', 0) > 60]

            # Sort filtered models by name
            sorted_models = sorted(filtered_models, key=lambda x: x.get('name', ''))

            # Print sorted models
            for model in sorted_models:
                print(f"Name: {model['name']}, Age: {model['age']}")

            logging.info("Filtered and sorted models successfully.")
        
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from file: {self.file_path}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

# Controller layer
class MainController:
    def __init__(self, number_service, string_service,model_service):
        self.number_service = number_service
        self.string_service = string_service
        self.model_service=model_service;

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

            # Process multiple numbers
            numbers_input = input("Enter a list of integers separated by commas: ").split(',')
            numbers = [num.strip() for num in numbers_input]
            processed_numbers = self.number_service.process_numbers(numbers)
            for result in processed_numbers:
                print(result)
            logging.info(f"Processed list of numbers: {numbers}")

            self.model_service.filter_and_sort_models()
        except ValueError as e:
            print(f"Error: {e}")
            logging.error(f"ValueError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logging.error(f"Unexpected error: {e} for inputs num: {num_input}, string: '{string}', numbers: {numbers_input}")

# Dependency injection and running the controller
if __name__ == "__main__":
    file_path = 'models.json'  # Replace with your JSON file path
    model_service = ModelService(file_path)
    number_service = NumberService()
    string_service = StringService()
    controller = MainController(number_service, string_service,model_service)
    controller.run()
