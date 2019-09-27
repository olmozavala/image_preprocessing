from os import listdir
from os.path import join
import os


def str2bool(cstr: str) -> bool:
    """It compares a string with anything like true, and it returns True or False"""
    return cstr in ['True', 'true', 't', True]

def get_id_number_from_cases(input_folder: str) -> list:
    """
    From a classic preproc folder containing Case-id, it obtains the
    number of the case (the id). It returns
    :param input_folder:
    :return:
    """
    cases = [int(x.split('-')[1]) for x in listdir(input_folder) if os.path.isdir(join(input_folder, x))]
    cases.sort()
    return cases
