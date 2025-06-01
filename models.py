import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the Menu model class
class Menu:
    def __init__(self, id, parent_id, name, created_date, updated_date, is_active, position, description,
                 image_state, main_page, link_is_active, link, main_image_id, menu_link, page_theme, lang,
                 meta_keywords, add_user_id, update_user_id):
        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.created_date = created_date
        self.updated_date = updated_date
        self.is_active = is_active
        self.position = position
        self.description = description
        self.image_state = image_state
        self.main_page = main_page
        self.link_is_active = link_is_active
        self.link = link
        self.main_image_id = main_image_id
        self.menu_link = menu_link
        self.page_theme = page_theme
        self.lang = lang
        self.meta_keywords = meta_keywords
        self.add_user_id = add_user_id
        self.update_user_id = update_user_id

    def __str__(self):
        return f"Menu(id={self.id}, name={self.name},  created_date={self.created_date}, updated_date={self.updated_date}, is_active={self.is_active})"

class Person:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person(id={self.id}, name={self.name}, age={self.age})"