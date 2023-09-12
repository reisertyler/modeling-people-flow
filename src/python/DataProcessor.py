####################################################################################################
"""

Author: TYLER REISER


"""
####################################################################################################

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

SAMPLE_FREQUENCY_LIST = [   '20Min', '10Min', '5Min', '2Min'    ]

class DataProcessor:
    '''
    A class to process the CU Boulder Network Information
    Date Created: Jul 28, 2023 
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
        data_mat             = pd.read_csv(file_path, header=None, names=['datetime', 'devicecount'])
        data_mat['datetime'] = pd.to_datetime(data_mat['datetime'])
        return data_mat

    def interpolate_time_series_data(self, data: pd.DataFrame) -> pd.DataFrame:
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
    

class SpeedTest:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        start_time = datetime.now()
        result = self.function(*self.args, **self.kwargs)
        end_time = datetime.now()
        total_time = end_time - start_time
        print(f"Time taken: {total_time}")
        return result

    def measure_data_processing_speed(self, sample_frequency_list=SAMPLE_FREQUENCY_LIST):
        num_cores       =   multiprocessing.cpu_count()
        core_list       =   list(   range(  1, num_cores + 1)   )
        times_record    =   { freq: [] for freq in sample_frequency_list  }
        exceptions      =   []

        with ProcessPoolExecutor(   max_workers = num_cores   ) as executor:

            data_processor = DataProcessor( cpu_cores    =   1, 
                                            sample_freq  =   sample_frequency_list[0],
                                            record_time  =   True)

            for frequency in sample_frequency_list:
                for core_num in core_list:
                    try:
                        data_processor.cpu_cores    = core_num
                        data_processor.sample_freq  = frequency

                        future      = executor.submit(  data_processor.process_all_buildings    )
                        total_time  = future.result()
                        
                        if isinstance(total_time, timedelta):
                            times_record[frequency].append(total_time.total_seconds())
                        else:
                            pass

                    except Exception as error:
                        exceptions.append(  (   core_num, frequency, str(error)    )   )
                        print(f"Error processing data with {core_num} cores and {frequency} frequency. Error: {error}")

        df_times = pd.DataFrame(times_record)

        plt.figure(     figsize =   (   12, 5   )       )
        for column in df_times.columns:
            sns.lineplot(data=df_times[column], label=column)

        plt.legend(title="Sample Frequency")

        plt.title(  "Data Processing Time by Sample Frequency for Number of Cores"   )
        plt.xlabel( "Number of CPU Cores"                       )
        plt.ylabel( "Time (seconds)"                            )

        plt.legend(     title   =   "Sample Frequency"  )
        plt.grid(True)
        plt.xlim(1, 10)
        
        ax = plt.gca()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        
        plt.show()

        if exceptions:
            print(  "Errors occurred during processing:"    )
            for core_num, frequency, error in exceptions:
                print(  f"Error processing data with {core_num} cores and {frequency} frequency. Error: {error}"    )

        return df_times