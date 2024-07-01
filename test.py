import logging
import json
# Service layer
from number_service import NumberService
from string_service import StringService
from model_service import ModelService
from menu_repository import MenuRepository
from data_structure import DataStructure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# Controller layer
class MainController:
    def __init__(self, number_service, string_service,model_service,menu_repository,data_structure):
        self.number_service = number_service
        self.string_service = string_service
        self.model_service=model_service
        self.menu_repository=menu_repository
        self.data_structure=data_structure

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

            self.model_service.process_persons()

            self.menu_repository.connect_and_process()
            self.data_structure.print_data_structure()
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
    menu_repository = MenuRepository()
    data_structure = DataStructure()
    controller = MainController(number_service, string_service,model_service,menu_repository,data_structure)
    controller.run()
