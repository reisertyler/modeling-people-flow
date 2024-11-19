

########################################################################
#
# AUTHOR:         TYLER A. REISER  
# CREATED:        SEPTEMBER   2023  
# MODIFIED:       NOVEMBER    2024
#
# COPYRIGHT (c) 2024 Tyler A. Reiser
#
########################################################################


"""

This module contains the DataReader, SparsityCalculator, and BuildingProcessor classes for processing, analyzing, and interpolating network information from the CU Boulder campus. 

Key functionalities of this module include:
- Reading time series data from a CSV file
- Interpolating the time series data
- Processing data for a specific building
- Processing data for all buildings
- Calculating the sparsity of the data
- Aggregating network data

The CSV files to be processed should be placed in the csv_directory specified when creating a DataReader object. The BuildingProcessor class can be used to process all buildings, calculate processing time, and calculate sparsity if required. The SparsityCalculator class is used to calculate the sparsity of the data.

"""

import os
import time
import multiprocessing
from datetime import datetime
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from joblib import Parallel, delayed
from pathlib import Path
from scipy.interpolate import UnivariateSpline


from src.python.processor.config_manager import ConfigManager
from src.python.processor.sparsity import SparsityCalculator


BASE_DIR = Path.cwd()

def build_path(*args):
    return BASE_DIR.joinpath(*args)


COMMON = '_Extracted_Data_8-16-2019.csv'

#CSV_DIRECTORY  = BASE_DIR.joinpath('data', 'input', 'CUT-CSV')
CSV_DIRECTORY   = BASE_DIR.joinpath('data', 'input', 'WiFiData-old')
#CSV_DIRECTORY  = BASE_DIR.joinpath('data', 'input', 'WiFiData-test')
OUTPUT_PATH     = BASE_DIR.joinpath('data', 'output', 'building-plots')


###############################################################################
#
#   Class: DataReader
#
###############################################################################

class DataReader:
    
    def __init__(
        self, 
        file_path  : Path      = CSV_DIRECTORY,
        start_date : datetime  = None, 
        end_date   : datetime  = None,
        config_name    = "Config1",
        config_file    = "config2.json",
        sample_freq    = "1Min"
        ):
        
        self.start_date         =   start_date
        self.end_date           =   end_date
        self.file_path          =   file_path
        self.config_manager     =   ConfigManager(config_file)
        self.config             =   self.config_manager.get_configuration(config_name)
        self.sample_freq        =   sample_freq
        self.save_interpolated  =   self.config[  'SAVE_INTERPOLATED' ]
        self.devicecount        =   self.config[  'DEVICECOUNT'       ]
        self.datetime           =   self.config[  'DATETIME'          ]
        self.save_directory     =   BASE_DIR.joinpath('data','output','interpolated-data')

    
    def read_time_series_data(self) -> pd.DataFrame:
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"No file found with the name {self.file_path}.")

        ##################################
        #   Read `CSV` files
        ##################################
        if self.file_path.suffix == '.csv':
            data_mat = pd.read_csv(self.file_path, header=None, names=[self.datetime, self.devicecount])

        ##################################
        #   Read `H5` files
        ################################## 
        elif self.file_path.suffix == '.h5':
            with h5py.File(self.file_path, 'r') as hdf:
                print("Keys of the .h5 file:")
                print(list(hdf.keys()))
                data_mat = hdf.get('dataset1')

        data_mat[self.datetime] = pd.to_datetime(data_mat[self.datetime])

        if self.start_date or self.end_date:
            data_mat = data_mat[(data_mat[self.datetime] >= self.start_date if self.start_date  else True) &
                                (data_mat[self.datetime] <= self.end_date   if self.end_date    else True)
                                ]
            
        return data_mat

    ##################################
    #   Linear interpolation
    ##################################
    def interpolate_time_series_data(self, data: pd.DataFrame) -> pd.DataFrame:
        
        # Get start and end date if none is passed
        if self.start_date is None or self.start_date < data.index.min():
            self.start_date = data.index.min()
            
        if self.end_date is None or self.end_date > data.index.max():
            self.end_date   = data.index.max()
        
        # LINEAR INTERPOLATION
        interpolation_range = pd.date_range(start=self.start_date, end=self.end_date, freq=self.sample_freq)
        f                   = interp1d(data.index.values.astype(float), data[self.devicecount],kind='linear')
        interpolated_values = f(interpolation_range.values.astype(float))
        interpolated_df     = pd.DataFrame(interpolated_values, index=interpolation_range, columns=[self.devicecount])
        
        # Save linearly interpolated data
        if self.save_interpolated:
            save_path   = "interpolated-data.csv"
            interpolated_df.to_csv(save_path)
            print('Interpolated data saved.')
            
        return interpolated_df


    ##################################
    #   Cubic-spline interpolation
    ##################################
    def smooth_time_series_data(self, data: pd.DataFrame, s: float = None) -> pd.DataFrame:
        
        # Get start and end date if none is passed
        if self.start_date is None or self.start_date < data.index.min():
           self.start_date  = data.index.min()
           
        if self.end_date is None or self.end_date > data.index.max():
           self.end_date    = data.index.max()
       
        # CUBLIC-SPLINE INTERPOLATION
        smoothing_range = pd.date_range(start=self.start_date, end=self.end_date, freq=self.sample_freq)
        s_spline        = UnivariateSpline(data.index.values.astype(float), data[self.devicecount], s=s)
        smoothed_values = s_spline(smoothing_range.values.astype(float))
        smoothed_df     = pd.DataFrame(smoothed_values, index=smoothing_range, columns=[self.devicecount])
       
        # Save linearly interpolated data 
        if self.save_interpolated:
            
            save_path   = "smoothed-data.csv"
            smoothed_df.to_csv(save_path)
            
            print('Smoothed data saved.')
            
        return smoothed_df


####################################################################################
#
#   Class: BuildingProcessor
#
####################################################################################

class BuildingProcessor:
    
    def __init__(
        self,
        data_reader: DataReader,
        building_id: str    = None, 
        use_common:  bool   = True, 
        cpu_cores:   int    = multiprocessing.cpu_count(), 
        record_time: bool   = False,
        sparsity_check: bool    = None,
        config_name             = "Config1",
        config_file             = "config2.json"
        ):
        
        self.data_reader    = data_reader
        self.building_id    = building_id
        self.use_common     = use_common
        self.cpu_cores      = cpu_cores
        self.record_time    = record_time
        self.sparsity_check = sparsity_check
        self.config_manager = ConfigManager(config_file)
        self.config         = self.config_manager.get_configuration(config_name)
        self.general        = self.config[  'GENERAL'       ]
        self.residential    = self.config[  'RESIDENTIAL'   ]
        self.community      = self.config[  'COMMUNITY'     ]
        self.start_date     = data_reader.start_date
        self.end_date       = data_reader.end_date 
        self.directories    = [
            BASE_DIR.joinpath('data',
                              'input',
                              'WiFiData-old', dir_name) for dir_name in ['Eduroam','UCBGuest','UCBWireless']
            ]
        
    def _get_building_identifiers(self, filename: str)  ->  str:
        return filename.split('_')[0]

    def _get_buildings(self, directory: Path)           ->  List[str]:
        filenames = os.listdir(directory)
        return [self._get_building_identifiers(filename) for filename in filenames]

    def _process_building_data(self, 
                               data_reader:     DataReader, 
                               building_name:   str, 
                               directory:       Path )  -> Tuple[str, pd.DataFrame]:
        
        csv_filename    = f"{building_name}{COMMON}" if self.use_common else building_name
        csv_filepath    = directory.joinpath(csv_filename)
        
        data_reader     = DataReader(file_path   = csv_filepath, 
                                     start_date  = self.start_date,
                                     end_date    = self.end_date,
                                     sample_freq = self.data_reader.sample_freq
                                     )
        
        try:
            data_mat = data_reader.read_time_series_data()
            data_mat = data_mat.set_index('datetime')
            
        except FileNotFoundError:
            print(f"No file found with the name {csv_filepath}.")
            return building_name
        
        if data_mat.empty:
            return building_name
        
        # INTERPOLATION
        #interpolated_data = data_reader.smooth_time_series_data(data_mat)
        interpolated_data = data_reader.interpolate_time_series_data(data_mat)
        
        if self.start_date or self.end_date:
            interpolated_data = interpolated_data[
                (interpolated_data.index >= self.start_date if self.start_date else True) &
                (interpolated_data.index <= self.end_date if self.end_date else True)
                ]
            
        return building_name, interpolated_data.reset_index().rename(columns={'index':'datetime'})


    def process_all_buildings(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        start_time  = time.time()
        results     = self.process_directories()
        results     = self.aggregate_network_data(results)
        total_time  = self.calculate_processing_time(start_time)
        
        # OUTPUT PRINTED 
        print(f"{total_time} seconds using {self.cpu_cores} CPU cores")

        if self.record_time:
            return total_time
        
        if self.sparsity_check:
            results = self.calculate_sparsity(results)
            
        return results


    def process_directories(self):
        results = {}
        
        for directory in self.directories:
            
            network_name    = os.path.basename(directory)
            building_list   = [self.building_id] if self.building_id else self._get_buildings(directory)
            
            network_results = Parallel(n_jobs=self.cpu_cores)(
                delayed(self._process_building_data)(
                    self.data_reader, building_name, directory) for building_name in building_list
                )
            
            results[network_name] = {k: v for k, v in network_results if not v.empty}
            
        return results
    
    
    ##################################
    #   - Network Aggregate
    #   - Building Sum
    #   - Building Grouping by Type
    #   - Campus Sum
    ##################################
    
    def aggregate_network_data(self, results):
        
        counts_type =   {   'general':      0, 
                            'residential':  0, 
                            'community':    0   
                            } 
        
        for network in  [   'Eduroam',  'UCBGuest', 'UCBWireless'   ]:
            if network in results:
                for building, df in results[network].items():
                    
                    #######################################
                    #   Determine building type
                    #######################################
                    building_type = None
                    
                    if building     in  self.general:
                        building_type   =   'general'
                        
                    elif building   in  self.residential:
                        building_type   =   'residential'
                        
                    elif building   in  self.community:
                        building_type   =   'community'
                    
                    #######################################
                    #   Update 'Sum' dictionary
                    ####################################### 
                    if 'Sum'    not in results:
                        results['Sum'] = {}
                        
                    if building not in results['Sum']:
                        results['Sum'][building] = df.copy()
                        
                    else:
                        results['Sum'][building]['devicecount'] += df['devicecount']
                     
                    #######################################
                    #   Update 'Type' dictionary
                    #######################################  
                    if 'Type'   not in results:
                        results['Type'] = {'general':       pd.DataFrame(), 
                                           'residential':   pd.DataFrame(), 
                                           'community':     pd.DataFrame()
                                           }

                    if building_type:
                        if results['Type'][building_type].empty:
                            results['Type'][building_type] = df.copy()
                            
                        else:
                            results['Type'][building_type]['devicecount'] += df['devicecount']
                        
                        # Increment count for this building type
                        counts_type[building_type] += 1
                        
                    #######################################
                    #   Update 'Campus' dictionary
                    #######################################  
                    if 'Campus' not in results:
                        results['Campus'] = df.copy()
                        
                    else:
                        results['Campus']['devicecount'] += df['devicecount']
        
        
        #######################################
        #   Calculating the average
        #######################################
                        
        # Initialize DataFrame for average for each building type
        if 'Average' not in results:
            results['Average'] =    {   'general':      pd.DataFrame(),
                                        'residential':  pd.DataFrame(),
                                        'community':    pd.DataFrame()
                                        }
            
        # Calculate average for each type of building 
        for building_type in ['general', 'residential', 'community']:
            
            if counts_type[building_type] > 0:
                temp_df = results['Type'][building_type].copy()
                
                # Calculate average
                temp_df[    'devicecount'   ] /= counts_type[building_type]
                
                # Store average in dictionary
                results[    'Average'       ][building_type] = temp_df    
        
        # PLOTTING AVERAGE     
        #plt.figure()
        #plt.plot(results['Average']['general']['devicecount'],      label='General'     )
        #plt.plot(results['Average']['residential']['devicecount'],  label='Residential' )
        #plt.plot(results['Average']['community']['devicecount'],    label='Community'   )
        #plt.legend()
        #plt.show()
        
        return results


    def calculate_processing_time(self, start_time):
        
        end_time = time.time()
        
        total_time          =   end_time - start_time
        total_time_rounded  =   np.round(total_time, 3)
        
        return total_time_rounded


    def calculate_sparsity(self, results):
        
        sparsity_calculator = SparsityCalculator()
        
        sparsity_results    = {
            network: sparsity_calculator.calculate_sparsity(v) if isinstance(v, pd.DataFrame) else {
                k: sparsity_calculator.calculate_sparsity(df) for k, df in v.items()} for network, v in results.items()
            }
        
        return sparsity_results
