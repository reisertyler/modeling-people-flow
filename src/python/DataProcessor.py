from src.python.utils import *


'''

A class to process the CU Boulder Network Information
Date Created: Jul 28, 2023 by T.Reiser

'''


class DataProcessor:
    
    def __init__(self,  
                 csv_directory: str     = CSV_DIRECTORY, 
                 start_date: datetime   = None, 
                 end_date: datetime     = None, 
                 building_id: str       = None, 
                 cpu_cores: int         = multiprocessing.cpu_count(),
                 sample_freq: str       = '10Min',
                 record_time: bool      = False):
        
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
        f                   = interp1d(data.index.values.astype(float), data['devicecount'], fill_value="extrapolate")
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
        results = Parallel(n_jobs=self.cpu_cores)(delayed(self._process_building_data)(building_name) for building_name in building_list)

        end_time    = datetime.now()
        total_time  = end_time - start_time

        if self.record_time:
            return total_time

        return {k: v for k, v in results if not v.empty}
