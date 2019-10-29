import os
from os import walk, listdir
from os.path import join
import pandas as pd

import numpy as np


def get_all_data(file_name, header_rows=0):
    print(F'Reading data from: {file_name}')
    data = pd.read_csv(file_name, header=header_rows)
    return data
