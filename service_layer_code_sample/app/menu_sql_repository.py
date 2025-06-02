# menu_repository.py
import pyodbc
import logging
from datetime import datetime
from app.models import Menu

class MenuSqlRepository:
    
    def get_mssql_connection(self,server, database, username, password):
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )
        return pyodbc.connect(connection_string)

    def fetch_menu_data(self,connection):
        query = """
        SELECT 
            Id, ParentId, Name, CreatedDate, UpdatedDate, IsActive, Position, Description, 
            ImageState, MainPage, LinkIsActive, Link, MainImageId, MenuLink, PageTheme, Lang, 
            MetaKeywords, AddUserId, UpdateUserId 
        FROM Menus
        """
        cursor = connection.cursor()
        cursor.execute(query)
        
        menus = []
        for row in cursor.fetchall():
            menu = Menu(
                id=row.Id,
                parent_id=row.ParentId,
                name=row.Name,
                created_date=row.CreatedDate,
                updated_date=row.UpdatedDate,
                is_active=row.IsActive,
                position=row.Position,
                description=row.Description,
                image_state=row.ImageState,
                main_page=row.MainPage,
                link_is_active=row.LinkIsActive,
                link=row.Link,
                main_image_id=row.MainImageId,
                menu_link=row.MenuLink,
                page_theme=row.PageTheme,
                lang=row.Lang,
                meta_keywords=row.MetaKeywords,
                add_user_id=row.AddUserId,
                update_user_id=row.UpdateUserId
            )
            menus.append(menu)
        
        cursor.close()
        return menus

    def connect_and_process(self):
        server = 'YUCE'
        database = 'eimece_2'
        username = 'test_admin'
        password = 'test_admin'

        try:
            connection = self.get_mssql_connection(server, database, username, password)
            menus = self.fetch_menu_data(connection)
            print('---------------------RESULT FROM DB--------------------------------')
            for menu in menus:
                print(f"Menu ID: {menu.id}, Name: {menu.name}, Created Date: {menu.created_date}")

            # Filter menus with id > 5100
            filtered_menus = [menu for menu in menus if menu.id > 4100]
            
            # Sort filtered menus by name
            sorted_menus = sorted(filtered_menus, key=lambda x: x.name)
            print('-------------------FILTERED AND SORTED MENU----------------------------------')
            # Print sorted menus
            for menu in sorted_menus:
                print(f"Menu ID: {menu.id}, Name: {menu.name}, Created Date: {menu.created_date}")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            if 'connection' in locals() and connection is not None:
                connection.close()
                logging.info("Database connection closed.")
        
    