
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
import logging
from typing import List
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import data.input.events.event_dict as ev
from src.python.time_series.plot_builder import DataFetcher, PlotCreator, PlotSaver
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

logger = logging.getLogger(__name__)


class DataVisualizer:
    def __init__(self, data_processor, config):
        self.data_processor = data_processor
        self.config         = config
        self.NETWORKS           = config['NETWORKS']
        self.FIGURE_SIZE        = tuple(config['FIGURE_SIZE'])
        self.SUBPLOT_ADJUSTMENT = config['SUBPLOT_ADJUSTMENT']
        self.LABEL_SIZES        = config['LABEL_SIZES']
        self.intervals          = config['INTERVALS']
        self.normalize          = config['NORMALIZE']
        self.show_plot          = config['SHOW_PLOT']
        self.devicecount        = config['DEVICECOUNT']
        self.COLORS             = config['COLORS']
        self.data_fetcher   = DataFetcher(self.data_processor) 
        self.event_plotter  = EventPlotter(config)
        self.plot_saver     = PlotSaver(config)
        self.plot_creator   = PlotCreator(config)

    def plot_single(self, building: str, networks: List[str]=None, events=ev.events):
        if networks is None:
            networks = self.NETWORKS
        dfs = []
        max_ys = []
        for network in networks:
            data = self.data_fetcher.fetch_building_data(network, building)
            if isinstance(data, pd.DataFrame):
                data.rename(columns={'datetime':'dt'}, inplace=True)
                dfs.append(data)
            else:
                logger.error(f"fetch_building_data returned a non-DataFrame for network {network} and building {building}: {data}")
                continue
        if not dfs or dfs[0].empty:
            logger.error(f"No data available for building {building}")
            return
        
        # Normalize and set y axis limit
        if self.normalize:
            scaler = MinMaxScaler()
            for df in dfs:
                df[self.devicecount] = scaler.fit_transform(df[self.devicecount].values.reshape(-1,1))
            max_ys = [1 for _ in dfs]     
        else:
            max_ys = [df[self.devicecount].max() for df in dfs]
            
        # Create the figure     
        fig, axs, start_date, end_date = self.plot_creator.create_plot(dfs[0], building)
        
        # Config 1 (Connected Time Series Plot):  
        #   Plot passed range of data on 1 plot
        if self.intervals == 1:
            if not isinstance(axs, list):
                axs = [axs]
            for df, max_y, network in zip(dfs, max_ys, networks):
                if df.empty:
                    continue
                    
                color = self.COLORS[network]
                self.plot_creator.plot_data(df, axs[0], building, 0, max_y, network, color)
                
        # Config 2 ("Chunked up" Time Series Plot):  
        #   Plot passed range of data subplots.
        else:
            if isinstance(axs, np.ndarray):
                axs = list(axs)
            for i, ax in enumerate(axs):
                start_index = i * len(dfs[0]) // self.intervals
                end_index = (i + 1) * len(dfs[0]) // self.intervals
                if start_index < 0 or end_index > len(dfs[0]):
                    logger.error("Invalid start_index or end_index")
                    return
                for df, max_y, network in zip(dfs, max_ys, networks):
                    if df.empty:
                        continue
                    color = self.COLORS[network]
                    self.plot_creator.plot_data(df, ax, building, i, max_y, network, color) 
                ax2 = ax.twinx()
                ax2.set_yticks([])
                if events is not None and isinstance(events, dict):
                    self.event_plotter.plot_events(df, ax2, events, max_y, start_index, end_index, pd.Timedelta(hours=3), pd.Timedelta(hours=3))
                    
        self.plot_saver.save_plot(building, start_date, end_date)  
        if self.show_plot:
            plt.show()
        else:
            plt.close()
        # folder_path = self.plot_saver.save_plot(building, start_date, end_date)         
        # return folder_path
      
  
class EventPlotter:
    def __init__(self,config):
        self.label_sizes = config['LABEL_SIZES']

    def plot_events(self, data_frame, axis, events, max_y_value, plot_start_index, 
                                                                 plot_end_index, 
                                                                 pre_event_interval,
                                                                 post_event_interval):
        if events is not None:
            color='grey'
            alpha=0.25
            dt_str=data_frame['dt'].dt.strftime('%Y-%m-%d')
            for event, dates in events.items():
                for year, date in dates.items():
                    event_date  = pd.to_datetime(date).strftime('%Y-%m-%d')
                    if dt_str.iloc[plot_start_index:plot_end_index].isin([event_date]).any():
                        event_index = dt_str[dt_str == event_date].index[0]
                        highlight_start_index = max(0,event_index-int(pre_event_interval.total_seconds() 
                                                                      / (data_frame['dt'].iloc[1]-data_frame['dt'].iloc[0]
                                                                         ).total_seconds()
                                                                      )
                                                    )
                        highlight_end_index = min(len(data_frame)-1, event_index+int(post_event_interval.total_seconds() 
                                                                                     / (data_frame['dt'].iloc[1]-data_frame['dt'].iloc[0]).total_seconds()
                                                                                     )
                                                  )
                        axis.fill_between(data_frame['dt'].iloc[highlight_start_index:highlight_end_index],0,max_y_value,color=color,alpha=alpha)
                        axis.text(data_frame['dt'].iloc[event_index],max_y_value-0.1*max_y_value,event,ha='center',va='bottom',fontsize=8)
            if axis.get_legend_handles_labels()[0]:
                axis.legend(loc='upper left')
                

class CampusPlotter:
    def __init__(self, data, config):
        self.data = data
        self.config = config
        self.output_path = config['OUTPUT_PATH']
        self.intervals = config['INTERVALS']
        self.figure_size = tuple(config['FIGURE_SIZE'])
        self.label_sizes = config['LABEL_SIZES']
        self.show_plot = config['SHOW_PLOT']
        self.normalize = config['NORMALIZE']
        self.devicecount = config['DEVICECOUNT']

    def normalize_device_count(self):
        if self.normalize:
            max_count = self.data[self.devicecount].max()
            min_count = self.data[self.devicecount].min()
            if max_count != min_count:
                self.data[self.devicecount] = (self.data[self.devicecount] - min_count) / (max_count - min_count)

    def create_output_dir(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def plot_phase_space(self):
        self.normalize_device_count()
        plt.figure(figsize=(6,6))
        plt.plot(self.data[self.devicecount][:-1], self.data[self.devicecount][1:], '#8B0000')
        plt.xlabel('x(t2)')
        plt.ylabel('x(t1)')
        plt.title('Phase space plot')
        plt.grid()
        self.create_output_dir()
        plt.savefig(f'{self.output_path}/phase_space.png')
        if self.show_plot:
            plt.show()

    def plot_data(self):
        self.normalize_device_count()
        fig, axs = plt.subplots(self.intervals, figsize=self.figure_size)
        plt.suptitle('77 Building Aggregate: Device Count vs. Time', fontsize=16, fontweight='bold')
        plt.subplots_adjust(hspace=0.25)
        split_data  = np.array_split(self.data, self.intervals)
        max_y       = self.data[self.devicecount].max()
        for i, data in enumerate(split_data):
            axs[i].plot(data['datetime'], data[self.devicecount],linewidth=2.0,color='#A50021', linestyle='-')
            axs[i].set_xlabel('Datetime')
            axs[i].set_ylabel('Device Count')
            axs[i].set_ylim([0, max_y])
            
            start_datetime  = data['datetime'].iloc[0].strftime('%b-%d-%Y')
            end_datetime    = data['datetime'].iloc[-1].strftime('%b-%d-%Y')
            axs[i].set_title(f"Building Aggregate: Device Count vs. Time - {start_datetime} to {end_datetime}")
            axs[i].xaxis.set_major_locator(mdates.MonthLocator())
            axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            axs[i].xaxis.set_minor_locator(mdates.DayLocator())
            axs[i].xaxis.set_minor_formatter(mdates.ConciseDateFormatter('%b'))
            axs[i].tick_params(axis='x',which='minor',labelsize=self.label_sizes['tick_params'])
            axs[i].grid(True)
        plt.tight_layout(pad=2.2)

        self.create_output_dir()
        plt.savefig(f'{self.output_path}/all-buildings.png')
        if self.show_plot:
            plt.show()