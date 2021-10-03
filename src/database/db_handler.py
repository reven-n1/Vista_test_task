import mysql.connector as connector


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


        except Exception as e:
            print(e)          
        

    def __create_tables(self):
        # type: () -> None
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        notebook.contacts(
            id int NOT NULL AUTO_INCREMENT, 
            user_id int NOT NULL ,
            full_name varchar(256) NOT NULL, 
            phone varchar(256) NOT NULL, 
            births_date date NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE KEY unique_record (user_id, full_name, phone, births_date), 
        CONSTRAINT contacts_to_user FOREIGN KEY (user_id) 
        REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE);
                            """)

        
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        notebook.users(
            id int NOT NULL AUTO_INCREMENT, 
            email varchar(256) NOT NULL, 
            password varchar(256) NOT NULL, 
            births_date date NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE KEY unique_users (email));
                            """)

        self.__db_connection.commit()
    
    
    def sign_up(self, email, password, births_date):
        # type: (str, str, str) -> None
        self.__cursor.execute("INSERT INTO notebook.users (email, password, births_date) VALUES('{em}', '{pas}', '{bth}')".format(em = email, pas = password, bth = births_date))
        self.__commit()


    def set_new_pass(self, new_password, email):
        # type: (str, str) -> None
        self.__cursor.execute("UPDATE notebook.users SET password = '{0}' WHERE email = '{1}'".format(new_password, email))
        self.__commit()


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



    def fetch_user(self, email):
        # type: (str) -> list
        self.__cursor.execute("SELECT email, password FROM notebook.users WHERE email = '{email}'".format(email=email))
        return self.__cursor.fetchone()


    def __commit(self):
        # type: () -> None
        self.__db_connection.commit()

    
    def __repr__(self):
         # type: () -> str
        return "{data} class - responsible for db processing".format(self.__class__.__name__)


    def __del__(self):
        self.__db_connection.close()
        

db = Database()
