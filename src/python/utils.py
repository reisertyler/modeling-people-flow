
'''

Imports, constants, and paths to directories.
Date Created: Jul 28, 2023 by T.Reiser

'''


import sys
import multiprocessing
from multiprocessing import Pool, cpu_count
import os
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from typing import List, Dict, Tuple

import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import PIL
from PIL import Image
from joblib import Parallel, delayed
from matplotlib import dates as mdates
import matplotlib.image as mpimg
from matplotlib.ticker import AutoMinorLocator
from scipy.interpolate import interp1d
from scipy import __version__ as scipy_version
from IPython.display import display

from matplotlib.dates import DateFormatter

from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize


def main():
    print(  'Python version:',        sys.version   )
    print(  'TensorFlow version:',    tf            )


COMMON        = '_Extracted_Data_8-16-2019.csv'
BASE_DIR      = os.getcwd()

def build_path(*args):
    return os.path.join(BASE_DIR, *args)

common_output_path = ['data', 'output', 'building-plots']
CSV_DIRECTORY = build_path('data', 'input', 'WiFiData')

OUTPUT_PATH_T_SERIES         = build_path( *common_output_path, 'intervals',    'time-series'     )
OUTPUT_PATH_DT_SERIES        = build_path( *common_output_path, 'intervals',    'datetime-series' )
OUTPUT_PATH_BUILDING_FULL_TS = build_path( *common_output_path, 'all-buildings'                   )
OUTPUT_PATH                  = build_path( *common_output_path                                    )

SAMPLE_FREQUENCY_LIST = ['15Min','10Min', '5Min']