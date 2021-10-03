from validation_exceptions import UserAlreadyExists, PassMissmatching, FiledsNotFullyFieled, UserNotFound, WrongPassword
from src.database.db_handler import db


def pass_validator(pass1, pass2):
    if pass1 != pass2:
        raise PassMissmatching


def fields_filling_validator(*args):
    for field in  args:
        if not field:
            raise FiledsNotFullyFieled 


def user_sign_in_validation(email, password):
    db_data = db.fetch_user(email)
    if not db_data:
        raise UserNotFound
    elif db_data[1] != password:
        raise WrongPassword


def user_exists_validation(email):
    db_data = db.fetch_user(email)
    if db_data:
        raise UserAlreadyExists


def change_pass_validator(email):
    db_data = db.fetch_user(email)
    if not db_data:
        raise UserNotFound