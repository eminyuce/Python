import logging
import json
# Service layer
from app.services.number_service import NumberService
from app.services.string_service import StringService
from app.services.json_service import JsonService
from app.repository.menu_sql_repository import MenuSqlRepository
from app.services.data_structure import DataStructure
from app.controllers.main_controller import MainController
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

 
# Dependency injection and running the controller
#  python service_main.py  it is how to run
if __name__ == "__main__":
    file_path = '../documents/models.json'  # Replace with your JSON file path
    json_service = JsonService(file_path)
    number_service = NumberService()
    string_service = StringService()
    menu_sql_repository = MenuSqlRepository()
    data_structure = DataStructure()
    controller = MainController(number_service, string_service,json_service,menu_sql_repository,data_structure)
    controller.run()
