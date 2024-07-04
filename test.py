import logging
import json
# Service layer
from number_service import NumberService
from string_service import StringService
from json_service import JsonService
from menu_sql_repository import MenuSqlRepository
from data_structure import DataStructure
from main_controller import MainController
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

 
# Dependency injection and running the controller
if __name__ == "__main__":
    file_path = 'models.json'  # Replace with your JSON file path
    json_service = JsonService(file_path)
    number_service = NumberService()
    string_service = StringService()
    menu_sql_repository = MenuSqlRepository()
    data_structure = DataStructure()
    controller = MainController(number_service, string_service,json_service,menu_sql_repository,data_structure)
    controller.run()
