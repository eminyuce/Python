import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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