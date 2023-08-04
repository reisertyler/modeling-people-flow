from src.python.DataProcessor import *


'''
Creating time-series plots for each building using parallel processing.
Date Created: Jul 28, 2023

    DataVisualizer is a class that visualizes data from buildings.

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

        plot_multiple           : plots data for multiple buildings' device count against time utilizing multiple cores.
            Args:
                building_list (list)    : list of building names. If not provided, all buildings are plotted.
                index_values (tuple)    : tuple containing start and end index. Default is 'all'.
                n_jobs (int)            : number of cores to be used for parallel execution. 
                                        : If not provided, all available cores will be used.
            Returns:
                None
'''


class DataVisualizer:

    def __init__(self, data_processor, show_plots=False, intervals=7):
        self.special_buildings = ['AERO', 'ATLS', 'C4C', 'LIBR', 'UMC', 'WLAW']
        self.data_processor = data_processor
        self.data           = self.data_processor.process_all_buildings()
        self.show_plots     = show_plots
        self.intervals      = intervals

    def fetch_building_names(self, building, index_values='all'):
        df = self.data[building]
        if index_values != 'all':
            df  = df.iloc[index_values[0]: index_values[1]]
        return df
    
    def time_to_seconds(self, time):
        return (time.hour * 60 + time.minute) * 60 + time.second
        
    def plot_single(self, building, index_values='all'):
        df          = self.fetch_building_names(building, index_values)
        df['dt']    = pd.to_datetime(df['datetime'])
        fig, axs    = plt.subplots(self.intervals, 1, figsize=(14, 20))

        fig.subplots_adjust(hspace=0.25)

        start_date      = df['dt'].iloc[  0 ].strftime( '%b-%d-%Y' )
        end_date        = df['dt'].iloc[ -1 ].strftime( '%b-%d-%Y' )
        building_title  = f": Device Count vs. Time " 
        date_title      = f"   -   {start_date} to {end_date}" 
        page_title      = building + building_title + date_title

        plt.suptitle(page_title, fontsize=14, fontweight='bold')
        plt.setp(axs, xlabel="Date", ylabel="Device Count")
        plt.tight_layout(pad=2.25)

        for i, ax in enumerate(axs):
            start_index =       i   * len(df)   //  self.intervals
            end_index   = ( i + 1 ) * len(df)   //  self.intervals
            split_df    = df.iloc[start_index:end_index]
            
            ax.plot(split_df["dt"], split_df["devicecount"], linewidth=0.7, label=building)
            
            ax.set_xlabel("Date",           fontsize=6)
            ax.set_ylabel("Device Count",   fontsize=6)

            interval_start  = split_df['dt'].iloc[  0   ].strftime('%b %d, %Y')
            interval_end    = split_df['dt'].iloc[  -1  ].strftime('%b %d, %Y')

            ax.set_title(f"Interval {i + 1} : {interval_start} to {interval_end}", fontsize=8)

            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            ax.xaxis.set_minor_locator(mdates.DayLocator())
            ax.xaxis.set_minor_formatter(mdates.ConciseDateFormatter('%b'))

            ax.tick_params(axis='both', which='major', labelsize=10)

        if self.show_plots:
            plt.show()
            
        else:
            folder_name_date        = f'{start_date}_to_{end_date}'
            folder_name_interval    = f'interval'
            folder_path             = os.path.join(OUTPUT_PATH, folder_name_date, folder_name_interval)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            if building in self.special_buildings:
                folder_path = os.path.join(OUTPUT_PATH, 'special', folder_name_date, folder_name_interval)
            else:
                folder_path = os.path.join(OUTPUT_PATH, folder_name_date, folder_name_interval)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, f'{building}.png') 

            plt.savefig(file_path)
            plt.close()
            return folder_path
        
  
    def plot_multiple(self, building_list=None, index_values='all', n_jobs=None):
        if n_jobs is None:
            n_jobs = multiprocessing.cpu_count()

        if building_list is None:
            building_list = list(self.data.keys())

        output_directories = Parallel(n_jobs=n_jobs)(delayed(self.plot_single)(building, index_values) for building in building_list)

        output_files = []
        for directory in output_directories:
            output_files.extend(os.listdir(directory))

        return output_files 
        