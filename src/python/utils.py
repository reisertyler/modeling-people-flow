import os
from typing import List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.stats import gaussian_kde
from sklearn.decomposition import NMF
import tensorflow as tf
from multiprocessing import Pool

import cmocean
import json
import pysindy as ps
import sklearn as sc
import multiprocessing
import scipy
import math

import datetime
from datetime import date, timedelta, datetime

# Constants
WEEKDAY_THRESHOLD = 5
COMMON = '_Extracted_Data_8-16-2019.csv'
DATA_PATH = './data/input/WiFiData/'

plt.style.use('bmh')

#########################################################################################
##                            PRINT STATEMENTS USED FOR CHECKS                         ##
#########################################################################################
##  Print dates, timestamps and data for the study that was built
#   
#   
def print_date(dates,ts,data):
    ##############
    # DATES      #
    ##############
    print("  --- Dates when data is collected:\n",      dates)
    n_dates = len(dates)
    print("  --- Number of days data is collected:",    n_dates)
    print("  --- First day data is collected:",         dates[0])
    print("  --- Last day data is collected:",          dates[n_dates-1])
    
    ##############
    # TIMESTAMPS #
    ##############
    print("\n--- Timestamps when data is recorded:\n",           ts)
    n_ts = len(ts)
    print("  --- Number of timestamps where data is collected:", n_ts)
    print("  --- First time data is collected:",                 ts[0])
    print("  --- Last time data is collected:",                  ts[n_ts-1])
    
    ##############
    # DATA       #
    ##############
    print("\n--- Data for each timestamp:\n",            np.round(data,2))
    n_data = len(data)
    print("  --- Number of timestamps",                  n_data)

    # Result: RETURN NUMBER OF TIMESTAMPS NEEDED
    n_data_entry = len(data[0])
    print("  --- Number of data entries at each timestamp:",      n_data_entry)
    return n_data_entry


#########################################################################################
######### THE FOLLOWING 4 FUNCTIONS JUST SPLIT THE LAST FUNCTION INTO 4 PIECES ##########
#########################################################################################
##  Three functions... 
#
#           1. DATES    2. TIMESTAMPS   3. DATA

def print_dates(dates):
    print("--- Dates when data is collected:\n",                 dates)
    n_dates = len(dates)
    print("--- Number of days data is collected:",               n_dates)
    print("--- First day data is collected:",                    dates[0])
    print("--- Last day data is collected:",                     dates[n_dates-1])

#   Print timestamps in the study built
def print_ts(ts):
    print("\n--- Timestamps when data is recorded:\n",           ts)
    n_ts = len(ts)
    print("--- Number of timestamps where data is collected:",   n_ts)
    print("--- First time data is collected:",                   ts[0])
    print("--- Last time data is collected:",                    ts[n_ts-1])

#   Print device count at each timestamp in the study built
def print_data(data):
    print("\n--- Data for each timestamp:\n",                    np.round(data,2))
    n_data = len(data)
    print("--- Number of timestamps",                            n_data)

    # Result: RETURN NUMBER OF TIMESTAMPS NEEDED
    n_data_entry = len(data[0])
    print("--- Number of data entries at each timestamp:",      n_data_entry)
    return n_data_entry


#########################################################################################
##                                   VERSION CHECK                                     ##
#########################################################################################
##  Print version information.
#   This package should also have a .yaml file or something that allows the user to 
#   replicate our results.
#  
#   *TensorFlow installation with GPU support on ARM architectures can be tricky but
#   the library should come into play soon. PyTorch didn't offer GPU support on ARM 
#   architectures early enough and I haven't looked into it.*
#   
#   OR 
# 
#   Get a CU Research Computing account and use the shared resources, where you can
#   load the modules on Alpine through 'ssh' or the OnDemand Terminal.
#
#   - CURC:
#   - OnDemand:
#
def print_versions():
    print(f"--------------- Version Check ---------------")
    print()
    print(f"Python      { sys.version       }")
    print()
    print(f"Numpy       { np.__version__    }")
    print(f"Pandas      { pd.__version__    }")
    print(f"PySINDy     { ps.__version__    }")
    print(f"SKLearn     { sc.__version__    }")
    print(f"SciPy       { scipy.__version__ }")
    print(f"Json        { json.__version__  }")
    print(f"TensorFlow  { tf.__version__    }")
    print()
    gpu = len(tf.config.list_physical_devices('GPU'))>0
    print("GPU is", "available" if gpu else "NOT AVAILABLE")
    print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
    print("Num CPUs Available: ", multiprocessing.cpu_count())
    print()
    print(f"----------------------------------------------")
