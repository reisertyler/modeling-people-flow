
"""
This module contains the DataProcessor class for processing and analyzing network information from the CU Boulder campus. 

Key functionalities of this module include:
- Reading time series data from a CSV file
- Interpolating the time series data
- Processing data for a specific building
- Processing data for all buildings

The CSV files to be processed should be placed in the csv_directory specified when creating a DataProcessor object.

Created on Jul 28, 2023.
"""


import os
import multiprocessing
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
from scipy.interpolate import interp1d
from joblib import Parallel, delayed
from concurrent.futures import ProcessPoolExecutor

BASE_DIR = os.getcwd()

def build_path(*args):
    return os.path.join(BASE_DIR, *args)

COMMON = '_Extracted_Data_8-16-2019.csv'
common_output_path = ['data', 'output', 'building-plots']
CSV_DIRECTORY = build_path('data', 'input', 'WiFiData')
OUTPUT_PATH = build_path( *common_output_path )


class DataProcessor:
    '''
    A class to process the CU Boulder Network Information

    Attributes:
    csv_directory (str): The directory where the CSV files are located.
    start_date (datetime): The start date for the data processing. Defaults to None.
    end_date (datetime): The end date for the data processing. Defaults to None.
    building_id (str): The id of the building to process data for. Defaults to None.
    cpu_cores (int): The number of CPU cores to use for processing. Defaults to the number of cores on the machine.
    sample_freq (str): The frequency for sampling the data. Defaults to '2Min'.
    record_time (bool): Whether to record the time taken for processing. Defaults to False.
    '''
    def __init__(self,  
                 csv_directory  : str       = CSV_DIRECTORY, 
                 start_date     : datetime  = None, 
                 end_date       : datetime  = None, 
                 building_id    : str       = None, 
                 cpu_cores      : int       = multiprocessing.cpu_count(),
                 sample_freq    : str       = '2Min',
                 record_time: bool          = False
                 ):
        
        self.csv_directory  = csv_directory
        self.start_date     = start_date
        self.end_date       = end_date
        self.building_id    = building_id
        self.cpu_cores      = cpu_cores
        self.sample_freq    = sample_freq
        self.record_time    = record_time

    @staticmethod
    def read_time_series_data(file_path: str) -> pd.DataFrame:
        """
        Reads time series data from a CSV file.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            pd.DataFrame: The time series data.
        """
        data_mat             = pd.read_csv(file_path, header=None, names=['datetime', 'devicecount'])
        data_mat['datetime'] = pd.to_datetime(data_mat['datetime'])
        return data_mat

    def interpolate_time_series_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Interpolates the time series data.

        Args:
            data (pd.DataFrame): The time series data.

        Returns:
            pd.DataFrame: The interpolated time series data.
        """
        data = data.loc[~data.index.duplicated(keep='first')]
        
        if self.start_date  is None:
            self.start_date = data.index.min()
            
        if self.end_date    is None:
            self.end_date   = data.index.max()
        
        interpolation_range = pd.date_range(start=self.start_date, end=self.end_date, freq=self.sample_freq)
        data.index          = data.index.tz_localize(None)
        f                   = interp1d(data.index.values.astype(float), data['devicecount'])
        interpolated_values = f(interpolation_range.values.astype(float))
        interpolated_df     = pd.DataFrame(interpolated_values, index=interpolation_range, columns=['devicecount'])
        
        return interpolated_df

    @staticmethod
    def _get_building_identifiers(filename: str) -> str:
        return filename.split('_')[0]

    def _get_buildings(self) -> List[str]:
        filenames = os.listdir(self.csv_directory)
        return [self._get_building_identifiers(filename) for filename in filenames]

    def _process_building_data(self, building_name: str) -> Tuple[str, pd.DataFrame]:
        csv_filepath = os.path.join(self.csv_directory, f"{building_name}{COMMON}")
        data_mat     = self.read_time_series_data(csv_filepath)
        data_mat     = data_mat.set_index('datetime')
        
        if data_mat.empty:
            return building_name, pd.DataFrame()

        interpolated_data = self.interpolate_time_series_data(data_mat)
        return building_name, interpolated_data.reset_index().rename(columns={'index':'datetime'})

    def process_all_buildings(self) -> Dict[str, pd.DataFrame]:
        start_time = datetime.now()

        building_list = [self.building_id] if self.building_id else self._get_buildings()
        results = Parallel(n_jobs=self.cpu_cores)(delayed(self._process_building_data)(building_name) 
                                                  for building_name in building_list
                                                  )

        end_time    = datetime.now()
        total_time  = end_time - start_time

        if self.record_time:
            return total_time

        return {k: v for k, v in results if not v.empty}