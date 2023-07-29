from src.python.utils import *
import src.python.DataProcessor as dp


class SingleVisualizer:

    def __init__(self, data_processor):
        self.data = data_processor.process_all_buildings()
 
    def data_matrix(self, building):
        df = self.data[building]
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['date'] = df['datetime'].dt.date
        df['time'] = df['datetime'].dt.time
        df['seconds'] = df['time'].apply(lambda t: t.hour*3600 + t.minute*60 + t.second)
        df = df.groupby(['date', 'seconds'])['devicecount'].mean().unstack()
        return df

    def plot_and_save(self, data_matrix, file_path):
        fig, ax = plt.subplots(figsize=(15, 8))
        for index, dayData in data_matrix.iterrows(): 
            ax.plot(dayData, label=index)

        ax.set_xlabel('Time')
        ax.set_ylabel('Device Count')
        ax.set_title('Device Count per day')
        ax.legend()
        
        start_date = data_matrix.index.min().strftime('%m-%Y')
        end_date = data_matrix.index.max().strftime('%m-%Y')
        folder_name = f'{start_date}_to_{end_date}'
        folder_path = os.path.join(OUTPUT_PATH, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        fig.savefig(os.path.join(folder_path, file_path))
        plt.close()

    def plot_multiple(self):
        for building in self.data.keys():
            day_data_matrix = self.data_matrix(building)
            file_path = f'{building}.png'
            self.plot_and_save(day_data_matrix, file_path)
