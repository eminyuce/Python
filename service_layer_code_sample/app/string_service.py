import logging
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StringService:
    def print_characters(self, string):
        for char in string:
            print(char)