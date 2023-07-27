import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple
from joblib import Parallel, delayed
import multiprocessing
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from scipy.interpolate import interp1d
from matplotlib.ticker import AutoMinorLocator
from concurrent.futures import ProcessPoolExecutor

COMMON        = '_Extracted_Data_8-16-2019.csv'
BASE_DIR      = os.getcwd()
CSV_DIRECTORY = os.path.join(BASE_DIR, 'data', 'input', 'WiFiData')
OUTPUT_PATH_T_SERIES = os.path.join(BASE_DIR, 'data', 'output', 'building-plots', 'time-series')
OUTPUT_PATH_DT_SERIES = os.path.join(BASE_DIR, 'data', 'output', 'building-plots', 'datetime-series')
OUTPUT_PATH   = os.path.join(BASE_DIR, 'data', 'output', 'building-plots')

SAMPLE_FREQUENCY_LIST = ['15Min','10Min','5Min','2Min','1Min']