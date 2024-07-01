import logging
import json
from models import Person
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelService:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_json_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            logging.info("Successfully loaded JSON data.")
            return data
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from file: {self.file_path}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

    def json_to_person_objects(self, data):
        persons = []
        for item in data:
            try:
                person = Person(
                    id=item.get('id'),
                    name=item.get('name'),
                    age=item.get('age')
                )
                persons.append(person)
            except KeyError as e:
                logging.error(f"Missing key in JSON data: {e}")
        return persons

    def filter_and_sort_persons(self, persons):
        # Filter persons with age > 60
        filtered_persons = [person for person in persons if person.age > 60]
        
        # Sort filtered persons by name
        sorted_persons = sorted(filtered_persons, key=lambda x: x.name)
        
        return sorted_persons

    def process_persons(self):
        try:
            data = self.load_json_data()
            persons = self.json_to_person_objects(data)
            sorted_persons = self.filter_and_sort_persons(persons)
            
            # Print sorted persons
            for person in sorted_persons:
                print(person)
            
            logging.info("Filtered and sorted persons successfully.")
        
        except Exception as e:
            logging.error(f"Unexpected error: {e}")