import os.path as path
import sys
from src.scripts.validation_exceptions import *


def pass_validator(pass1, pass2):
    if pass1 != pass2:
        raise PassMissmatching


def fields_filling_validator(*args):
    for field in  args:
        if not field:
            raise FiledsNotFullyFieled 
