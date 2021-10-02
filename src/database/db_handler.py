import mysql.connector as connector
from json import load

class Database(object):

    def __init__(self):
        try:
            self.__db_connection = connector.connect(
                user = "user",
                password = "pass",
                host = "localhost",
                port = "3306",                 
            )

            self.__cursor = self.__db_connection.cursor()

            self.__create_tables()

        except FileNotFoundError:
            pass

        except Exception as e:
            print(e)          
        

    def __create_tables(self):
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        phonebook.users (
            id int(10) unsigned NOT NULL AUTO_INCREMENT,
            email varchar(255) NOT NULL,
            password varchar(255) NOT NULL,
            births_date date NOT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY unique_users (email)
            ) ENGINE = InnoDB AUTO_INCREMENT = 13 DEFAULT CHARSET = utf8mb4;
                            """)

        
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        phonebook.contacts (
            id int(10) unsigned NOT NULL AUTO_INCREMENT,
            user_id int(10) unsigned NOT NULL,
            full_name varchar(255) NOT NULL,
            phone varchar(255) NOT NULL,
            births_date date NOT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY unique_records (user_id, full_name, phone, births_date),
            CONSTRAINT contacts_to_users FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON
            UPDATE
                CASCADE
            ) ENGINE = InnoDB AUTO_INCREMENT = 19 DEFAULT CHARSET = utf8mb4;
                            """)

        self.__db_connection.commit()
    

    
    
    def sign_in(self, request):
        # type: (str) -> None
        pass

    
    def sign_up(self, email, password, births_date):
        # type: (str) -> None
        pass


    def get_all_contacts(self, request):
        # type: (str) -> None
        pass


    def get_nearest_birthds(self, request):
        # type: (str) -> None
        pass


    def add_contact(self, request):
        # type: (str) -> None
        pass


    def edit_contact(self, request):
        # type: (str) -> None
        pass


    def del_contact(self, request):
        # type: (str) -> None
        pass


    def __commit(self):
        self.__db_connection.commit()

    
    def __repr__(self):
         # type: () -> str
        return "{data} class - responsible for db processing".format(self.__class__.__name__)


    def __del__(self):
        self.__db_connection.close()
        

db = Database()