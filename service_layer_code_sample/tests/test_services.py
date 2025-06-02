import unittest
from unittest.mock import mock_open, patch, call
import json
import logging
from io import StringIO

from service_layer_code_sample.app.controllers.main_controller import MainController
from service_layer_code_sample.app.services.number_service import NumberService
from service_layer_code_sample.string_service import StringService
from service_layer_code_sample.json_service import JsonService
from service_layer_code_sample.app.repository.menu_sql_repository import MenuSqlRepository
from service_layer_code_sample.data_structure import DataStructure


# Configure logging to capture logs for testing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestNumberService(unittest.TestCase):
    def setUp(self):
        self.number_service = NumberService()

    def test_check_even_odd_even(self):
        result = self.number_service.check_even_odd(4)
        self.assertEqual(result, "4 is even.")

    def test_check_even_odd_odd(self):
        result = self.number_service.check_even_odd(5)
        self.assertEqual(result, "5 is odd.")

    def test_factorial_positive(self):
        result = self.number_service.factorial(5)
        self.assertEqual(result, 120)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            self.number_service.factorial(-1)

    def test_process_numbers(self):
        numbers = ["2", "3", "abc"]
        with self.assertRaises(ValueError):
            self.number_service.process_numbers(numbers)

    def test_is_integer(self):
        self.assertTrue(self.number_service.is_integer("4"))
        self.assertFalse(self.number_service.is_integer("abc"))

class TestStringService(unittest.TestCase):
    def setUp(self):
        self.string_service = StringService()

    @patch('builtins.print')
    def test_print_characters(self, mock_print):
        self.string_service.print_characters("hello")
        mock_print.assert_has_calls([call('h'), call('e'), call('l'), call('l'), call('o')])

class TestModelService(unittest.TestCase):
    def setUp(self):
        self.file_path = 'models.json'
        self.json_service = JsonService(self.file_path)
        self.mock_json_data = '''
        [
            {"name": "Alice", "age": 65},
            {"name": "Bob", "age": 55},
            {"name": "Charlie", "age": 70},
            {"name": "David", "age": 62},
            {"name": "Eve", "age": 58}
        ]
        '''

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_file_not_found(self, mock_file):
        with patch('json.load', side_effect=FileNotFoundError):
            result = self.json_service.filter_and_sort_models()
            self.assertEqual(result, [])
            self.assertLogs(level='ERROR')

    @patch('builtins.open', new_callable=mock_open, read_data='Invalid JSON')
    def test_json_decode_error(self, mock_file):
        with patch('json.load', side_effect=json.JSONDecodeError('Expecting value', 'Invalid JSON', 0)):
            result = self.model_service.filter_and_sort_models()
            self.assertEqual(result, [])
            self.assertLogs(level='ERROR')

    @patch('builtins.open', new_callable=mock_open, read_data='''
    [
        {"name": "Alice", "age": 65},
        {"name": "Bob", "age": 55},
        {"name": "Charlie", "age": 70},
        {"name": "David", "age": 62},
        {"name": "Eve", "age": 58}
    ]
    ''')
    @patch('builtins.print')
    def test_filter_and_sort_models(self, mock_print, mock_file):
        self.model_service.filter_and_sort_models()
        expected_calls = [call('Name: Alice, Age: 65'), call('Name: Charlie, Age: 70'), call('Name: David, Age: 62')]
        mock_print.assert_has_calls(expected_calls)

class TestMainController(unittest.TestCase):
    @patch('builtins.input', side_effect=["4", "hello", "1,2,abc"])
    @patch('builtins.print')
    def test_run(self, mock_print, mock_input):

        file_path = 'models.json'  # Replace with your JSON file path
        json_service = JsonService(file_path)
        number_service = NumberService()
        string_service = StringService()
        menu_sql_repository = MenuSqlRepository()
        data_structure = DataStructure()
        controller = MainController(number_service, string_service,json_service,menu_sql_repository,data_structure)

        with self.assertRaises(ValueError):
            controller.run()

if __name__ == '__main__':
    unittest.main()
