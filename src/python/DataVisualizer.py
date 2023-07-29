from src.python.DataProcessor import *


'''

Creating time-series plots for each building using parallel processing.
Date Created: Jul 28, 2023 by T.Reiser

'''


class DataVisualizer:
    """
    A class that visualizes data from live buildings.

    Attributes:
        data_processor (Object) : instance of data processor class to process the data.
        show_plots (boolean)    : whether to show plots or not. Default is False.
        intervals (int)         : number of intervals for division and plotting.
        data (DataFrame)        : processed data loaded inside the class.

    Methods:
        fetch_building_names    : fetches data for a particular building.
        data_matrix             : generate data matrix for a building based on device count.
        time_to_seconds         : converts the provided time into equivalent seconds.
        plot_single             : plots a single building's device count against time.
        plot_multiple           : plots multiple buildings' device count against time.
    """

    def __init__(self, data_processor, show_plots=False, intervals=7):
        """Initialize the class with data_processor, show_plots status and number of intervals."""
        
        self.data_processor = data_processor
        self.data           = self.data_processor.process_all_buildings()
        self.show_plots     = show_plots
        self.intervals      = intervals

    def fetch_building_names(self, building, index_values='all'):
        """Fetches data for a particular building.
        
        Args:
            building (str)       : Name of the building.
            index_values (tuple) : tuple containing start and end index. Default is 'all'.
        
        Returns:
            df (DataFrame) : filtered data for the building.
        """
        df = self.data[building]
        if index_values != 'all':
            df  = df.iloc[index_values[0]: index_values[1]]
        return df
    
    
    def time_to_seconds(self, time):
        """Converts the given time to seconds.
        
        Args:
            time (Time) : time object
            
        Returns:
            int : equivalent seconds for the provided time.
        """
        
        return (time.hour * 60 + time.minute) * 60 + time.second
        
    def plot_single(self, building, index_values='all'):
        """
        Generate a plot for the single building.

        Args:
            building (str)       : name of the building.
            index_values (tuple) : start and end index for data slicing. Default is 'all'.

        Returns:
            None
        """
        
        df          = self.fetch_building_names(    building,   index_values    )
        df['dt']    = pd.to_datetime(   df['datetime']  )
        
        fig, axs    = plt.subplots(self.intervals, 1, figsize=(10, 15))

        for i, ax in enumerate(axs):
            start_index =       i   * len(df)   //  self.intervals
            end_index   = ( i + 1 ) * len(df)   //  self.intervals
            split_df    = df.iloc[start_index:end_index]
            
            ax.plot(split_df["dt"], split_df["devicecount"], linewidth=0.5, label=building)
            
            ax.set( title   =   f"Interval {i + 1} : {split_df['dt'].iloc[0]} to {split_df['dt'].iloc[-1]}", 
                   xlabel   =   "Date", 
                   ylabel   =   "Device Count"  
                   )

            ax.xaxis.set_major_locator  (   mdates.MonthLocator()       )
            ax.xaxis.set_major_formatter(   mdates.DateFormatter('%m')  )
            ax.xaxis.set_minor_locator  (   mdates.DayLocator()         )

        plt.suptitle( building + ": Device Count vs. Time", fontsize=9, fontweight='bold' )

        start_date  = df['dt'].iloc[  0 ].strftime( '%m-%Y' )
        end_date    = df['dt'].iloc[ -1 ].strftime( '%m-%Y' )

        if self.show_plots:
            plt.show()
            
        else:
            start_date  = df['dt'].iloc[  0 ].strftime( '%m-%Y' )
            end_date    = df['dt'].iloc[ -1 ].strftime( '%m-%Y' )
            folder_name = f'{start_date}_{end_date}'
            folder_path = os.path.join(OUTPUT_PATH_DT_SERIES, folder_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, f'{building}.png') 

            plt.savefig(file_path)
            plt.close()
            
            
    def plot_df(self, building, x, y, xlabel, ylabel, plot_df_file_path):
        """
        Plot a two-dimensional line graph using matplotlib. Include start and end dates in title and filename.

        Parameters:
        self (someClass): Represents the instance of the class. By convention, it is often named 'self'.
        building (str): The name of the building. Used for the filename of the saved plot image.
        x (list or equivalent): The data for the x-axis. Assumed to be a list of datetime values.
        y (list or equivalent): The data for the y-axis
        xlabel (str): The label for the x-axis, default is 'Date'.
        ylabel (str): The label for the y-axis, default is 'Device Count'.

        Returns:
        None
        """
        
        plt.figure(figsize=(15, 5))
        plt.plot(x, y,  color='orange', linewidth=0.5)
        
        start_date  = x.iloc[   0   ].strftime( '%m-%Y' )
        end_date    = x.iloc[   -1  ].strftime( '%m-%Y' )

        plt.gca().set(title=f"{start_date} to {end_date}", xlabel=xlabel, ylabel=ylabel)
        plt.suptitle(f"{building}: Device Count vs. Time", fontsize=9, fontweight='bold')
        start_date  = x.iloc[   0   ].strftime( '%m-%Y' )
        end_date    = x.iloc[   -1  ].strftime( '%m-%Y' )
        folder_name = f'{start_date}_{end_date}'
        folder_path = os.path.join(OUTPUT_PATH_BUILDING_FULL_TS, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, f'{building}.png') 

        plt.savefig(plot_df_file_path)
        plt.close()
        
  
    def plot_multiple(self, building_list=None, index_values='all', n_jobs=None):
        """
        Plot data for multiple buildings utilizing multiple cores.

        Args:
            building_list (list): list of building names. If not provided, all buildings are plotted.
            index_values (tuple): tuple containing start and end index. Default is 'all'.
            n_jobs (int)        : number of cores to be used for parallel execution. If not provided, all available cores will be used.

        Returns:
            None
        """
        import matplotlib.dates as mdates

        if n_jobs is None:
            n_jobs = multiprocessing.cpu_count()

        if building_list is None:
            building_list = list(self.data.keys())

        Parallel(n_jobs=n_jobs)(delayed(self.plot_single)(building, index_values) for building in building_list)

        for building in building_list:
            df          = self.fetch_building_names(building, index_values) 
            df['dt']    = pd.to_datetime(df['datetime'])
            x           = df['dt']
            y           = df['devicecount']
            title       = building + ": Device Count vs. Time"
            stitle      = "Detailed View"
            xlabel      = "Date"
            ylabel      = "Device Count"

            start_date  = x.iloc[0].strftime('%m-%Y')
            end_date    = x.iloc[-1].strftime('%m-%Y')
            folder_name = f'{start_date}_{end_date}'
            
            folder_path_1 = os.path.join(OUTPUT_PATH_BUILDING_FULL_TS, folder_name)
            
            if not os.path.exists(folder_path_1):
                os.makedirs(folder_path_1)
            
            plot_df_file_path = os.path.join(folder_path_1, f'{building}.png') 
            self.plot_df(building, x, y, xlabel, ylabel, plot_df_file_path)