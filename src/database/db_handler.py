#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.scripts.validation_exceptions import NoNearestBirth
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


    def get_all_contacts(self, email):
        # type: (str) -> list
        self.__cursor.execute("SELECT full_name, phone, contacts.births_date FROM notebook.contacts join \
        notebook.users on contacts.user_id = users.id WHERE users.email = '{0}'".format(email))
        return self.__cursor.fetchall()

    
    def get_contacts_count(self, email):
        # type: (str) -> int
        self.__cursor.execute("SELECT COUNT(users.id) FROM notebook.contacts join \
        notebook.users on contacts.user_id = users.id WHERE users.email = '{0}'".format(email))
        res = int(self.__cursor.fetchone()[0])
        return 0 if not res else res


    def get_nearest_birthds(self, email):
        # type: (str) -> list
        self.__cursor.execute("SELECT full_name, phone, contacts.births_date FROM notebook.contacts join \
        notebook.users on contacts.user_id = users.id WHERE users.email = '{0}' \
        AND DayOfYear(contacts.births_date) BETWEEN DayOfYear(NOW()) and DayOfYear(NOW() + INTERVAL 7 DAY)".format(email))
        res = self.__cursor.fetchall()
        if res:
            return res
        else:
            raise NoNearestBirth


    def add_contact(self, name, phone, births_date, email):
        # type: (str, str, str, str) -> None
        self.__cursor.execute(u"INSERT INTO notebook.contacts (user_id, full_name, phone ,births_date) \
             VALUES((SELECT id FROM notebook.users WHERE email = '{0}'), '{1}', '{2}', '{3}')".format(email, name, phone, births_date))
        self.__commit()


    def edit_contact(self, new_name, new_phone, new_births_date, rec_id):
        # type: (str, str, str, str) -> None
        self.__cursor.execute("UPDATE notebook.contacts SET full_name = '{0}' , phone = '{1}' , births_date = '{2}' \
        WHERE id = '{3}'".format(new_name, str(new_phone), new_births_date, int(rec_id)))
        self.__commit()
    

    def get_record_id(self, name, phone, births_date):
        # type: (str, str, str) -> list
        self.__cursor.execute("SELECT id FROM notebook.contacts WHERE full_name = '{0}' AND phone = '{1}' AND births_date = '{2}'".format(name, str(phone), births_date))
        return self.__cursor.fetchone()[0]


    def del_contact(self, rec_id):
        # type: (str) -> None
        self.__cursor.execute("DELETE FROM notebook.contacts WHERE id = {0}".format(int(rec_id)))
        self.__commit()


    def fetch_user(self, email):
        # type: (str) -> tuple
        self.__cursor.execute("SELECT email, password FROM notebook.users WHERE email = '{email}'".format(email=email))
        return self.__cursor.fetchone()

    
    def contact_exists(self, name, phone, births_date, email):
        # type: (str, str, str, str) -> tuple
        self.__cursor.execute(u"SELECT full_name, phone, contacts.births_date FROM notebook.contacts join \
        notebook.users on contacts.user_id = users.id WHERE users.email = '{0}' \
        AND full_name = '{1}' AND contacts.births_date = '{2}' AND phone = '{3}'".format(email, name, births_date, phone))
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
