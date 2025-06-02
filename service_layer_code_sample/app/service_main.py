import logging
import json
# Service layer
from app.number_service import NumberService
from app.string_service import StringService
from app.json_service import JsonService
from app.menu_sql_repository import MenuSqlRepository
from app.data_structure import DataStructure
from app.main_controller import MainController
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

 
# Dependency injection and running the controller
if __name__ == "__main__":
    file_path = '../documents/models.json'  # Replace with your JSON file path
    json_service = JsonService(file_path)
    number_service = NumberService()
    string_service = StringService()
    menu_sql_repository = MenuSqlRepository()
    data_structure = DataStructure()
    controller = MainController(number_service, string_service,json_service,menu_sql_repository,data_structure)
    controller.run()
