
from src.python.DataProcessor import *

class DataVisualizer:

    def __init__(self, data_processor, show_plots=False, intervals=7):
        self.data_processor = data_processor
        self.data = self.data_processor.process_all_buildings()
        self.show_plots = show_plots
        self.intervals = intervals

    def grab(self, building, index_values='all'):
        df = self.data[building]
        if index_values != 'all':
            df  = df.iloc[index_values[0]: index_values[1]]
        return df

    def data_matrix(self, building):
        df = self.data[building]
        df['time']  = pd.to_datetime(df['datetime']).dt.time
        data_matrix = df.groupby('time')['devicecount'].apply(list).values
        return data_matrix
    
    def time_to_seconds(self, time):
        return (time.hour * 60 + time.minute) * 60 + time.second
        
    def plot_single(self, building, index_values='all'):
        df = self.grab(building, index_values)
        df['dt'] = pd.to_datetime(df['datetime'])

        fig, axs = plt.subplots(self.intervals, 1, figsize=(10, 15))

        for i, ax in enumerate(axs):
            start_index = i * len(df)     // self.intervals
            end_index = (i + 1) * len(df) // self.intervals 
            split_df = df.iloc[start_index:end_index]
            ax.plot(split_df["dt"], split_df["devicecount"], linewidth=0.5, label=building)
            ax.set(title=f"Interval {i + 1}: {split_df['dt'].iloc[0]} to {split_df['dt'].iloc[-1]}", xlabel="Date", ylabel="Device Count")

            ax.xaxis.set_major_locator (mdates.MonthLocator())
            ax.xaxis.set_major_formatter(   mdates.DateFormatter('%m'))
            ax.xaxis.set_minor_locator(mdates.DayLocator())

        plt.suptitle(building + ": Device Count vs. Time", fontsize=9, fontweight='bold')

        start_date = df['dt'].iloc[0].strftime('%m-%Y')
        end_date = df['dt'].iloc[-1].strftime('%m-%Y')

        if self.show_plots:
            plt.show()
        else:
            plt.savefig(f'{OUTPUT_PATH_DT_SERIES}/{building}_{start_date}_{end_date}.png')
            plt.close()
  
    def plot_multiple(self, building_list=None, index_values='all'):
        if building_list is None:
            building_list = list(self.data.keys())
        Parallel(n_jobs=10)(delayed(self.plot_single)(building, index_values) for building in building_list)