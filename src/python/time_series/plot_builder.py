
########################################################################
#
# AUTHOR:         TYLER A. REISER  
# CREATED:        SEPTEMBER   2023  
# MODIFIED:       NOVEMBER    2024
#
# COPYRIGHT (c) 2024 Tyler A. Reiser
#
########################################################################

""" COPYRIGHT 2024 Tyler A Reiser. """

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class DataFetcher:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.data = self.data_processor.process_all_buildings()

    def fetch_building_data(self, network, building):
        if network not in self.data:
            print(f"No data for network {network}")
            return None
        if building not in self.data[network]:
            print(f"No data for building {building} in network {network}")
            return None
        try:
            df = pd.DataFrame(self.data[network][building])
        except Exception as e:
            print(f"Error creating DataFrame for network {network} and building {building}: {e}")
            return None
        if df.empty:
            print(f"DataFrame for network {network} and building {building} is empty")
            return None
        return df


class PlotCreator:
    def __init__(self, config):
        self.intervals          = config['INTERVALS']
        self.figure_size        = tuple(config['FIGURE_SIZE'])
        self.subplot_adjustment = config['SUBPLOT_ADJUSTMENT']
        self.label_sizes        = config['LABEL_SIZES']

    def create_plot(self, df, building):
            fig, axs = plt.subplots(self.intervals, 1, figsize=self.figure_size, dpi=360)
            fig.subplots_adjust(hspace=self.subplot_adjustment)
            start_datetime  = df['dt'].iloc[ 0].strftime('%b-%d-%Y')
            end_datetime    = df['dt'].iloc[-1].strftime('%b-%d-%Y')
            building_title  = f": Device Count vs. Time "
            page_title_date = f" - {start_datetime } to {end_datetime }"
            page_title      = building + building_title + page_title_date
            plt.suptitle(page_title, fontsize=16, fontweight='bold')
            plt.setp(axs, xlabel="Date (Month/Day)", ylabel="Device Count")
            plt.tight_layout(pad=2.2)
            return fig, axs, start_datetime, end_datetime 
        
    def plot_data(self, df, ax, building, i, max_y, network, color): 
        start_index     = (i    )   * len(df)   // self.intervals
        end_index       = (i + 1)   * len(df)   // self.intervals
        split_df        = df.iloc[start_index:end_index]
        
        ax.set_ylim([0, max_y]) 
        ax.plot(split_df["dt"], split_df["devicecount"], linewidth=0.8, color=color, label=network)
        ax.set_xlabel("Date (Month/Day)", fontsize=self.label_sizes['xlabel'])
        ax.set_ylabel("Device Count", fontsize=self.label_sizes['ylabel'])
        
        interval_start  = split_df['dt'].iloc[0].strftime('%b %d, %Y')
        interval_end    = split_df['dt'].iloc[-1].strftime('%b %d, %Y')
        
        ax.set_title(f"{building}: Device Count vs. Time  - {interval_start} to {interval_end}", fontsize=self.label_sizes['title'])
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.xaxis.set_minor_formatter(mdates.ConciseDateFormatter('%b'))
        ax.tick_params(axis='x', which='minor', labelsize=self.label_sizes['tick_params'])
        ax.grid(True)
        ax.legend()


class PlotSaver:
    def __init__(self, config):
        self.output_path = config['OUTPUT_PATH']
        self.general     = config['GENERAL']
        self.residential = config['RESIDENTIAL']
        self.community   = config['COMMUNITY']
        self.not_good    = config['NOT_GOOD']
        self.folder_name_interval    = config['FOLDER_NAME_INTERVAL']

    def save_plot(self, building, start_date, end_date):
        folder_name_date        = f'{start_date}_to_{end_date}'
        folder_path             = os.path.join(self.output_path,folder_name_date,self.folder_name_interval)

        if building in self.general:
            folder_path = os.path.join(folder_path,'class_and_admin')
        if building in self.residential:
            folder_path = os.path.join(folder_path,'residential')
        if building in self.community:
            folder_path = os.path.join(folder_path,'community')
        if building in self.not_good:
            folder_path = os.path.join(folder_path,'excluded')
            
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f'{building}.png')
        
        try:
            plt.savefig(file_path, dpi=360)
            print(f"{building}\tsaved to: {folder_path}")
        except Exception as e:
            print(f"Error saving plot to {folder_path}: {e}")
            return None
        return folder_path 